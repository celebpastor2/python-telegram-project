import os
import csv
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegramSocial.settings")
django.setup()

from telegramApp.models import Products

# Path to your Documents/product.csv
csv_file = os.path.expanduser("~/Documents/products.csv")

def import_products():
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            product, created = Products.objects.get_or_create(
                product_name=row["product_name"],
                defaults={
                    "product_id": row.get("product_id", ""),
                    "departmet_id": row.get("department_id", ""),
                    "price": row.get("price", 0),
                    "aisle_id": row.get("aisle_id", ""),
                },
            )
            if created:
                print(f"✅ Added product: {product.name}")
            else:
                print(f"⚠️ Product already exists: {product.name}")

if __name__ == "__main__":
    import_products()
