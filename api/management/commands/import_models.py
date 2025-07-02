# your_app/management/commands/import_models_from_excel.py

import base64
import re
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import pandas as pd
from django.utils import timezone
from django.core.files import File
from django.core.files.base import ContentFile

import os

class Command(BaseCommand):
    help = 'Import model data from Excel with image field support'

    def handle(self, *args, **kwargs):
        app_label = 'api'  # Change to your app name
        file_path = os.path.join(settings.BASE_DIR, f'{app_label}_models.xlsx')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        excel_file = pd.ExcelFile(file_path)
        model_map = {model.__name__: model for model in apps.get_app_config(app_label).get_models()}
        now = timezone.now()

        for sheet_name in excel_file.sheet_names:
            model = model_map.get(sheet_name)
            if not model:
                self.stdout.write(self.style.WARNING(f"Skipping unknown model sheet: {sheet_name}"))
                continue

            df = excel_file.parse(sheet_name)

            if 'created_at' in df.columns:
                df['created_at'] = now
            if 'updated_at' in df.columns:
                df['updated_at'] = now

            image_fields = [f.name for f in model._meta.fields if f.get_internal_type() == 'ImageField']

            for _, row in df.iterrows():
                data = row.dropna().to_dict()

                obj = model()  # Create empty instance
                for field, value in data.items():
                    if field in image_fields:
                        if value and isinstance(value, str) and value.startswith("data:image"):
                            # Extract base64 data and file extension
                            match = re.match(r'data:image/(?P<ext>\w+);base64,(?P<data>.+)', value)
                            if match:
                                ext = match.group('ext')
                                img_data = match.group('data')
                                img_content = base64.b64decode(img_data)
                                file_name = f"{field}.{ext}"
                                getattr(obj, field).save(file_name, ContentFile(img_content), save=False)
                            else:
                                self.stdout.write(self.style.WARNING(f"Invalid base64 image data for field: {field}"))
                        else:
                            # Fallback: treat as file path (legacy support)
                            image_path = os.path.join(settings.MEDIA_ROOT, str(value))
                            if os.path.exists(image_path):
                                with open(image_path, 'rb') as img_file:
                                    getattr(obj, field).save(os.path.basename(image_path), File(img_file), save=False)
                            else:
                                self.stdout.write(self.style.WARNING(f"Image not found: {image_path}"))
                    else:
                        setattr(obj, field, value)
                obj.save()
            self.stdout.write(self.style.SUCCESS(f"Imported data into model: {sheet_name}"))
