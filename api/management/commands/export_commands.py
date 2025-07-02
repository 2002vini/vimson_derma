import base64
import datetime
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.apps import apps
import pandas as pd
from django.utils.timezone import is_aware
from django.db import models



class Command(BaseCommand):
    help = 'Export all models in the app to an Excel file'

    def handle(self, *args, **options):
        app_label = 'api'  # Change to your app's name
        model_list = apps.get_app_config(app_label).get_models()

        output_file = f'{app_label}_models.xlsx'

        with pd.ExcelWriter(output_file, engine='openpyxl') as excel_writer:
            for model in model_list:
                model_name = model.__name__
                print(f'Exporting model: {model_name}')
                
                queryset = model.objects.all()
                
                image_fields = []
                for field in model._meta.get_fields():
                    if isinstance(field, models.ImageField):
                        image_fields.append(field.name)
                        
                data = pd.DataFrame(list(queryset.values()))

                # Convert image fields to base64
                for img_field in image_fields:
                    if img_field in data.columns:
                        def img_to_base64(img_path):
                            if not img_path:
                                return ""
                            # Build the full path to the image
                            full_path = os.path.join(settings.MEDIA_ROOT, img_path)
                            if os.path.isfile(full_path):
                                with open(full_path, "rb") as image_file:
                                    encoded = base64.b64encode(image_file.read()).decode('utf-8')
                                    ext = os.path.splitext(full_path)[1][1:]  # e.g. 'jpg'
                                    return f"data:image/{ext};base64,{encoded}"
                            return ""
                        print(f'Converting images for field: {img_field}')
                        data[img_field] = data[img_field].apply(img_to_base64)
                        print(f'Converted images for field: {data[img_field]}')


                # Remove timezone from datetime columns
                for col in data.columns:
                    if pd.api.types.is_datetime64_any_dtype(data[col]):
                            data[col] = pd.Timestamp.now()

                data.to_excel(excel_writer, sheet_name=model_name[:31], index=False)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported models to {output_file}'))
