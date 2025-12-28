#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eCommerce.settings')
django.setup()

from products.models import Product, Category

print("=== DATABASE CHECK ===")
print(f"Categories: {Category.objects.all().count()}")
print(f"Products: {Product.objects.all().count()}")
print(f"Products with categories: {Product.objects.exclude(category=None).count()}")

print("\n=== CATEGORIES ===")
for cat in Category.objects.all():
    print(f"- {cat.name}: {cat.product_set.count()} products")

print("\n=== SAMPLE PRODUCTS ===")
for product in Product.objects.all()[:5]:
    print(f"- {product.title}: Category = {product.category}")