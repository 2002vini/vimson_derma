import csv
from datetime import datetime

# Input and output files
input_file = 'FACE_CARE_PRODUCTS.txt'
output_file = 'oralcare_products_output.csv'

# Get current datetime in ISO format
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Column headers
headers = [
    "NAME",
    "DESCRIPTION",
    "CATEGORY",
    "IMAGE",
    "IS FEATURED",
    "CREATED AT",
    "UPDATED AT",
    "ATTRIBUTES"
]

# Process input
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=headers)
    writer.writeheader()

    for line in infile:
        name = line.strip()
        if not name:
            continue

        row = {
            "NAME": name,
            "DESCRIPTION": "None",
            "CATEGORY": "OralCare",
            "IMAGE": f"media/products/medicated/Oralcare/{name}.webp",
            "IS FEATURED": "False",
            "CREATED AT": current_time,
            "UPDATED AT": current_time,
            "ATTRIBUTES": ""
        }

        writer.writerow(row)

print(f"✅ Done! {output_file} created with product data.")
