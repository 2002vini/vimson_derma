import csv
from datetime import datetime
from django.utils.timezone import make_aware
from api.models import Product, Category

csv_path = 'api/management/commands/oralcare_products_output.csv'  # Update this path

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        name = row['NAME'].strip()
        description = row['DESCRIPTION'] if row['DESCRIPTION'] != 'None' else ''
        category_name = row['CATEGORY'].strip()
        image_path = row['IMAGE'].strip()
        is_featured = False
        created_at = make_aware(datetime.strptime(row['CREATED AT'], '%Y-%m-%d %H:%M:%S'))
        updated_at = make_aware(datetime.strptime(row['UPDATED AT'], '%Y-%m-%d %H:%M:%S'))
        attributes = row['ATTRIBUTES'] if row['ATTRIBUTES'].strip() else None

        category, _ = Category.objects.get_or_create(type=category_name)

        product, created = Product.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'category': category,
                'image': image_path,
                'is_featured': is_featured,
                'created_at': created_at,
                'updated_at': updated_at,
                'attributes': attributes,
                'is_medicated': True,  # or True if applicable
                'is_customized': False,
                'tagline': ''
            }
        )

        if created:
            print(f"✅ Created: {name}")
        else:
            print(f"⚠️ Skipped (already exists): {name}")
