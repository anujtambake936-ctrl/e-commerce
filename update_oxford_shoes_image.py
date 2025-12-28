#!/usr/bin/env python3
"""
Update the image for Oxford Dress Shoes product.

Usage (PowerShell):
    cd C:\\Users\\anujt\\django-ecommerce
    .\\venv-ecommerce\\Scripts\\Activate.ps1
    python update_oxford_shoes_image.py
"""
import os
import sys
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify

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

# Better image URL for Oxford shoes
OXFORD_SHOES_IMAGE_URL = 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&h=600&fit=crop&crop=center'

def main():
    try:
        # Find the Oxford Dress Shoes product
        product = Product.objects.filter(title__icontains='oxford').first()
        
        if not product:
            print("Oxford Dress Shoes product not found!")
            return
        
        print(f"Found product: {product.title}")
        print(f"Current image: {product.image.name if product.image else 'No image'}")
        print(f"\nUpdating image from: {OXFORD_SHOES_IMAGE_URL}")
        
        # Download new image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(OXFORD_SHOES_IMAGE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Create filename
        filename = f"{slugify(product.title)}.jpg"
        
        # Save new image
        product.image.save(filename, ContentFile(response.content), save=True)
        
        print(f"✓ Successfully updated image: {filename}")
        print(f"New image path: {product.image.url}")
        
    except Product.DoesNotExist:
        print("Error: Oxford Dress Shoes product not found in database.")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

