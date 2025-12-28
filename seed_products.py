#!/usr/bin/env python3
"""
Seed sample Product rows into the project's SQLite database.

Usage (PowerShell):
    cd C:\\Users\\anujt\\django-ecommerce
    .\\venv-ecommerce\\Scripts\\Activate.ps1
    python seed_products.py

The script uses the Django ORM and will create products if they do not already exist.
"""
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eCommerce.settings')

try:
    import django
    django.setup()
except Exception as e:
    print("Error: could not configure Django. Make sure you're running this with your project's virtualenv activated.")
    print(e)
    sys.exit(1)

from products.models import Product

SAMPLES = [
    {
        "title": "Blue Trainers",
        "brand": "SportCo",
        "price": 59.99,
        "description": "Comfortable trainers for everyday use",
        "size": "9",
        "color": "Blue",
    },
    {
        "title": "White Hoodie",
        "brand": "StreetWear",
        "price": 39.99,
        "description": "Cozy hoodie for cold days",
        "size": "L",
        "color": "White",
    },
    {
        "title": "Classic Watch",
        "brand": "TimeCo",
        "price": 129.99,
        "description": "Elegant wrist watch with leather strap",
        "size": "",
        "color": "Silver",
    },
]


def main():
    created = []
    for s in SAMPLES:
        obj, was_created = Product.objects.get_or_create(
            title=s['title'],
            defaults={
                'brand': s['brand'],
                'price': s['price'],
                'description': s['description'],
                'size': s['size'],
                'color': s['color'],
            }
        )
        created.append((obj.id, obj.title, was_created))
        print(f"{'Created' if was_created else 'Exists:'} {obj.id} - {obj.title}")

    total = Product.objects.count()
    print('\nSummary:')
    print(f'  Total products in DB: {total}')


if __name__ == '__main__':
    main()
