import requests
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product, Category
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate products with better data for clothing, footwear, and accessories'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate products with better data...')
        
        # Clear existing products
        Product.objects.all().delete()
        
        # Create categories first
        categories_data = [
            {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and apparel items'},
            {'name': 'Footwear', 'slug': 'footwear', 'description': 'Shoes and footwear'},
            {'name': 'Accessories', 'slug': 'accessories', 'description': 'Fashion accessories, jewelry, watches, and more'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            categories[cat_data['name'].lower()] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Sample products data with better categorization
        products_data = [
            # Clothing
            {
                'title': 'Classic White T-Shirt',
                'price': 19.99,
                'description': 'Premium cotton white t-shirt with comfortable fit. Perfect for casual wear.',
                'category': 'clothing',
                'brand': 'BasicWear',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop'
            },
            {
                'title': 'Denim Jacket',
                'price': 79.99,
                'description': 'Classic blue denim jacket with vintage wash. Timeless style for any wardrobe.',
                'category': 'clothing',
                'brand': 'DenimCo',
                'image_url': 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop'
            },
            {
                'title': 'Cotton Hoodie',
                'price': 49.99,
                'description': 'Comfortable cotton hoodie with drawstring hood. Perfect for casual outings.',
                'category': 'clothing',
                'brand': 'ComfortWear',
                'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop'
            },
            {
                'title': 'Casual Button Shirt',
                'price': 39.99,
                'description': 'Lightweight casual shirt with button-down collar. Great for work or weekend.',
                'category': 'clothing',
                'brand': 'CasualFit',
                'image_url': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=400&fit=crop'
            },
            {
                'title': 'Summer Dress',
                'price': 59.99,
                'description': 'Flowy summer dress with floral pattern. Perfect for warm weather occasions.',
                'category': 'clothing',
                'brand': 'SummerStyle',
                'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop'
            },
            {
                'title': 'Slim Fit Jeans',
                'price': 69.99,
                'description': 'Modern slim fit jeans with stretch fabric. Comfortable and stylish.',
                'category': 'clothing',
                'brand': 'ModernFit',
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop'
            },
            
            # Footwear
            {
                'title': 'Running Sneakers',
                'price': 89.99,
                'description': 'Lightweight running sneakers with cushioned sole. Perfect for daily workouts.',
                'category': 'footwear',
                'brand': 'SportRun',
                'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop'
            },
            {
                'title': 'Leather Boots',
                'price': 129.99,
                'description': 'Premium leather boots with durable construction. Great for outdoor activities.',
                'category': 'footwear',
                'brand': 'LeatherCraft',
                'image_url': 'https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=400&h=400&fit=crop'
            },
            {
                'title': 'Canvas Sneakers',
                'price': 45.99,
                'description': 'Classic canvas sneakers with rubber sole. Timeless casual footwear.',
                'category': 'footwear',
                'brand': 'ClassicStep',
                'image_url': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=400&fit=crop'
            },
            {
                'title': 'Formal Oxford Shoes',
                'price': 149.99,
                'description': 'Elegant oxford shoes in genuine leather. Perfect for business and formal events.',
                'category': 'footwear',
                'brand': 'FormalStep',
                'image_url': 'https://images.unsplash.com/photo-1614252369475-531eba835eb1?w=400&h=400&fit=crop'
            },
            
            # Accessories
            {
                'title': 'Classic Wristwatch',
                'price': 199.99,
                'description': 'Elegant stainless steel watch with leather strap. Timeless design for any occasion.',
                'category': 'accessories',
                'brand': 'TimeClassic',
                'image_url': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=400&fit=crop'
            },
            {
                'title': 'Leather Wallet',
                'price': 49.99,
                'description': 'Premium leather wallet with multiple card slots. Compact and functional design.',
                'category': 'accessories',
                'brand': 'LeatherGoods',
                'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=400&fit=crop'
            },
            {
                'title': 'Sunglasses',
                'price': 79.99,
                'description': 'UV protection sunglasses with polarized lenses. Stylish and functional.',
                'category': 'accessories',
                'brand': 'SunStyle',
                'image_url': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop'
            },
            {
                'title': 'Silver Chain Bracelet',
                'price': 89.99,
                'description': 'Sterling silver chain bracelet with elegant design. Perfect for everyday wear.',
                'category': 'accessories',
                'brand': 'SilverCraft',
                'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop'
            },
            {
                'title': 'Leather Belt',
                'price': 39.99,
                'description': 'Genuine leather belt with classic buckle. Essential accessory for any wardrobe.',
                'category': 'accessories',
                'brand': 'BeltCraft',
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop'
            },
            {
                'title': 'Baseball Cap',
                'price': 24.99,
                'description': 'Adjustable baseball cap with embroidered logo. Perfect for casual outings.',
                'category': 'accessories',
                'brand': 'CapStyle',
                'image_url': 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop'
            },
        ]
        
        # Create products
        for product_data in products_data:
            category = categories[product_data['category']]
            
            # Create product
            product = Product.objects.create(
                title=product_data['title'],
                category=category,
                brand=product_data['brand'],
                price=product_data['price'],
                description=product_data['description'],
                featured=product_data['price'] > 100,  # Mark expensive items as featured
                active=True
            )
            
            # Download and save image
            try:
                img_response = requests.get(product_data['image_url'])
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
        
        # Print final counts
        self.stdout.write(f"\nFinal category counts:")
        for cat_name, category in categories.items():
            count = category.product_set.count()
            self.stdout.write(f"{category.name}: {count} products")
        
        self.stdout.write(self.style.SUCCESS('Successfully populated products with better data!'))