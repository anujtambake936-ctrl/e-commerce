#!/usr/bin/env python3
"""
Add images to existing products that don't have images.

Usage (PowerShell):
    cd C:\\Users\\anujt\\django-ecommerce
    .\\venv-ecommerce\\Scripts\\Activate.ps1
    python add_images_to_products.py
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

# Image URLs based on product keywords
IMAGE_MAPPING = {
    # Clothing
    'shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop&crop=center',
    'henley': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop&crop=center',
    'jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=500&fit=crop&crop=center',
    'denim': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=500&fit=crop&crop=center',
    'sweater': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=500&fit=crop&crop=center',
    'wool': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=500&fit=crop&crop=center',
    'dress': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=500&fit=crop&crop=center',
    'hoodie': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=500&fit=crop&crop=center',
    'cotton': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop&crop=center',
    
    # Footwear
    'shoe': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=500&fit=crop&crop=center',
    'sneaker': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=500&fit=crop&crop=center',
    'boot': 'https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=400&h=500&fit=crop&crop=center',
    'trainer': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=500&fit=crop&crop=center',
    'oxford': 'https://images.unsplash.com/photo-1614252369475-531eba835eb1?w=400&h=500&fit=crop&crop=center',
    'running': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=500&fit=crop&crop=center',
    'canvas': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=500&fit=crop&crop=center',
    
    # Accessories
    'watch': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=500&fit=crop&crop=center',
    'wallet': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=500&fit=crop&crop=center',
    'sunglass': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=500&fit=crop&crop=center',
    'necklace': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=500&fit=crop&crop=center',
    'jewelry': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=500&fit=crop&crop=center',
    'silver': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=500&fit=crop&crop=center',
    'gold': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=500&fit=crop&crop=center',
    
    # Default
    'default': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=500&fit=crop&crop=center',
}

def get_image_url(product):
    """Get appropriate image URL based on product title and description."""
    text = f"{product.title} {product.description}".lower()
    
    # Check for matching keywords
    for keyword, url in IMAGE_MAPPING.items():
        if keyword in text:
            return url
    
    # Return default if no match
    return IMAGE_MAPPING['default']


def main():
    products = Product.objects.all()
    products_needing_images = []
    
    # Find products that need images
    for product in products:
        # Check if product has default image or no image
        if not product.image or product.image.name == 'default.png' or 'default' in product.image.name.lower():
            products_needing_images.append(product)
    
    if not products_needing_images:
        print("All products already have images!")
        return
    
    print(f"Found {len(products_needing_images)} products that need images.")
    print("\nAdding images...\n")
    
    success_count = 0
    error_count = 0
    
    for product in products_needing_images:
        try:
            image_url = get_image_url(product)
            print(f"Processing: {product.title}")
            print(f"  Image URL: {image_url}")
            
            # Download image
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(image_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Create filename
            filename = f"{slugify(product.title)}.jpg"
            
            # Save image
            product.image.save(filename, ContentFile(response.content), save=True)
            
            print(f"  ✓ Successfully added image: {filename}\n")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}\n")
            error_count += 1
    
    print("\n" + "="*50)
    print("Summary:")
    print(f"  Successfully added images: {success_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total products: {Product.objects.count()}")
    print("="*50)


if __name__ == '__main__':
    main()

