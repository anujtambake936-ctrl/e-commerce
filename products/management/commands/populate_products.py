import requests
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product, Category
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate products from FakeStore API'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate products from API...')
        
        # Create categories first
        categories_data = [
            {'name': 'Clothing', 'description': 'Fashion and apparel items'},
            {'name': 'Footwear', 'description': 'Shoes and footwear'},
            {'name': 'Accessories', 'description': 'Fashion accessories and jewelry'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name'].lower()] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Fetch products from FakeStore API
        try:
            response = requests.get('https://fakestoreapi.com/products')
            response.raise_for_status()
            products_data = response.json()
            
            for product_data in products_data:
                # Map API categories to our categories
                api_category = product_data.get('category', '').lower()
                category = None
                
                if 'clothing' in api_category or 'clothes' in api_category:
                    category = categories['clothing']
                elif 'shoe' in api_category or 'footwear' in api_category:
                    category = categories['footwear']
                elif 'jewelry' in api_category or 'accessories' in api_category:
                    category = categories['accessories']
                else:
                    # Default to clothing for unknown categories
                    category = categories['clothing']
                
                # Check if product already exists
                if Product.objects.filter(title=product_data['title']).exists():
                    self.stdout.write(f'Product already exists: {product_data["title"]}')
                    continue
                
                # Create product
                product = Product.objects.create(
                    title=product_data['title'],
                    category=category,
                    brand='Generic',  # API doesn't provide brand
                    price=float(product_data['price']),
                    description=product_data['description'],
                    featured=product_data.get('rating', {}).get('rate', 0) > 4.0,
                    active=True
                )
                
                # Download and save image
                try:
                    img_response = requests.get(product_data['image'])
                    img_response.raise_for_status()
                    
                    # Create filename from product title
                    filename = f"{slugify(product_data['title'])}.jpg"
                    
                    # Save image
                    product.image.save(
                        filename,
                        ContentFile(img_response.content),
                        save=True
                    )
                    
                    self.stdout.write(f'Created product: {product.title}')
                    
                except Exception as e:
                    self.stdout.write(f'Error downloading image for {product.title}: {str(e)}')
                    # Keep the product but with default image
                    
        except requests.RequestException as e:
            self.stdout.write(f'Error fetching products from API: {str(e)}')
            return
        
        self.stdout.write(self.style.SUCCESS('Successfully populated products!'))