import csv
from datetime import datetime
from django.utils.timezone import make_aware
from api.models import Product, Category

csv_path = '/Users/vinihundlani/Desktop/vimson_derma/api/management/commands/products_output.csv'  # Replace with the actual file path
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        name = row['NAME'].strip()
        description = row['DESCRIPTION'] if row['DESCRIPTION'] != 'None' else ''
        category_name = row['CATEGORY'].strip()
        image_path = row['IMAGE'].strip()
        is_featured = False
        updated_at = current_time  # Assuming updated_at is the same as current time
        attributes = row['ATTRIBUTES'] if row['ATTRIBUTES'].strip() else None

        category, _ = Category.objects.get_or_create(type=category_name)

        try:
            product = Product.objects.get(name=name)
            product.description = description
            product.category = category
            product.image = image_path
            product.is_featured = is_featured
            product.updated_at = updated_at
            product.attributes = attributes
            product.is_medicated = True  # Assuming this is always True for the given data  
            product.save()
            print(f"✅ Updated: {name}")
        except Product.DoesNotExist:
            print(f"❌ Product not found (skipped): {name}")
