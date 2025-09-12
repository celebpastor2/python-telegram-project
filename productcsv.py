import os
import csv
import requests

# Setup Django environment
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegramSocial.telegramSocial.settings")
#django.setup()

#from telegramSocial.telegramApp.models import Products

# Path to your Documents/product.csv
csv_file = os.path.join(os.getcwd(), "products.csv")

def import_products():
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            requests.post('http://localhost:8000/submit-product', row)
            break
            

if __name__ == "__main__":
    import_products()
