import requests
import time
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product, Category
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate fashion store with high-quality products using Unsplash API'

    def handle(self, *args, **options):
        self.stdout.write('🛍️ Starting Fashion Store Population...')
        
        # Clear existing products
        deleted_count = Product.objects.count()
        Product.objects.all().delete()
        self.stdout.write(f'✅ Cleared {deleted_count} existing products')
        
        # Create/get categories
        clothing, _ = Category.objects.get_or_create(
            name='Clothing',
            defaults={'slug': 'clothing', 'description': 'Premium fashion and apparel', 'active': True}
        )
        footwear, _ = Category.objects.get_or_create(
            name='Footwear', 
            defaults={'slug': 'footwear', 'description': 'Designer shoes and boots', 'active': True}
        )
        accessories, _ = Category.objects.get_or_create(
            name='Accessories',
            defaults={'slug': 'accessories', 'description': 'Luxury accessories and jewelry', 'active': True}
        )
        
        # High-quality fashion products with Unsplash images
        fashion_products = [
            # PREMIUM CLOTHING
            {
                'title': 'Premium Cotton Henley',
                'category': clothing,
                'brand': 'StyleCraft',
                'price': 45.99,
                'description': 'Soft organic cotton henley with button placket. Perfect for casual elegance.',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'Classic Denim Jacket',
                'category': clothing,
                'brand': 'DenimWorks',
                'price': 89.99,
                'description': 'Vintage-inspired denim jacket with authentic wash and premium details.',
                'image_url': 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=500&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'Merino Wool Sweater',
                'category': clothing,
                'brand': 'WoolCraft',
                'price': 129.99,
                'description': 'Luxurious merino wool sweater with ribbed details. Incredibly soft and warm.',
                'image_url': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Elegant Midi Dress',
                'category': clothing,
                'brand': 'ElegantWear',
                'price': 159.99,
                'description': 'Sophisticated midi dress perfect for office or evening occasions.',
                'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Casual Button-Down',
                'category': clothing,
                'brand': 'CasualFit',
                'price': 65.99,
                'description': 'Versatile button-down shirt in premium cotton. Great for any occasion.',
                'image_url': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=500&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'Designer Blazer',
                'category': clothing,
                'brand': 'FormalStyle',
                'price': 199.99,
                'description': 'Tailored blazer with modern cut and premium fabric blend.',
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            
            # PREMIUM FOOTWEAR
            {
                'title': 'Performance Running Shoes',
                'category': footwear,
                'brand': 'SportTech',
                'price': 149.99,
                'description': 'Advanced running shoes with responsive cushioning and breathable mesh.',
                'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Handcrafted Leather Boots',
                'category': footwear,
                'brand': 'BootCraft',
                'price': 249.99,
                'description': 'Premium leather boots with Goodyear welt construction. Built to last.',
                'image_url': 'https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Classic Canvas Sneakers',
                'category': footwear,
                'brand': 'CanvasKing',
                'price': 79.99,
                'description': 'Timeless canvas sneakers with vulcanized rubber sole and vintage appeal.',
                'image_url': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=500&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'Oxford Dress Shoes',
                'category': footwear,
                'brand': 'FormalStep',
                'price': 189.99,
                'description': 'Elegant oxford shoes in genuine leather for business and formal events.',
                'image_url': 'https://images.unsplash.com/photo-1614252369475-531eba835eb1?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Athletic Sneakers',
                'category': footwear,
                'brand': 'ActiveWear',
                'price': 119.99,
                'description': 'Modern athletic sneakers with superior comfort and style.',
                'image_url': 'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400&h=500&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'Chelsea Boots',
                'category': footwear,
                'brand': 'UrbanStep',
                'price': 169.99,
                'description': 'Sleek chelsea boots with elastic side panels and premium leather.',
                'image_url': 'https://images.unsplash.com/photo-1582897085656-c636d006a246?w=400&h=500&fit=crop&crop=center',
                'featured': False
            },
            
            # LUXURY ACCESSORIES
            {
                'title': 'Swiss Automatic Watch',
                'category': accessories,
                'brand': 'SwissTime',
                'price': 599.99,
                'description': 'Precision Swiss automatic watch with sapphire crystal and steel case.',
                'image_url': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Italian Leather Wallet',
                'category': accessories,
                'brand': 'LeatherCraft',
                'price': 89.99,
                'description': 'Handcrafted Italian leather wallet with RFID protection and card slots.',
                'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=500&fit=crop&crop=center',
                'featured': False
            },
            {
                'title': 'Designer Sunglasses',
                'category': accessories,
                'brand': 'LuxeVision',
                'price': 179.99,
                'description': 'Premium designer sunglasses with polarized lenses and UV400 protection.',
                'image_url': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Sterling Silver Necklace',
                'category': accessories,
                'brand': 'SilverCraft',
                'price': 149.99,
                'description': 'Elegant sterling silver necklace with modern pendant design.',
                'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Leather Crossbody Bag',
                'category': accessories,
                'brand': 'BagCraft',
                'price': 219.99,
                'description': 'Premium leather crossbody bag with adjustable strap and compartments.',
                'image_url': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400&h=500&fit=crop&crop=center',
                'featured': True
            },
            {
                'title': 'Classic Leather Belt',
                'category': accessories,
                'brand': 'BeltMaster',
                'price': 59.99,
                'description': 'Genuine leather belt with polished buckle. Perfect for any outfit.',
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=500&fit=crop&crop=center',
                'featured': False
            },
        ]
        
        self.stdout.write('📦 Creating fashion products...')
        created_count = 0
        
        for product_data in fashion_products:
            try:
                # Create product
                product = Product.objects.create(
                    title=product_data['title'],
                    category=product_data['category'],
                    brand=product_data['brand'],
                    price=product_data['price'],
                    description=product_data['description'],
                    featured=product_data['featured'],
                    active=True
                )
                
                # Download and save image
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    response = requests.get(product_data['image_url'], headers=headers, timeout=15)
                    response.raise_for_status()
                    
                    filename = f"{slugify(product_data['title'])}.jpg"
                    product.image.save(filename, ContentFile(response.content), save=True)
                    
                    status = "⭐ FEATURED" if product.featured else "📦 REGULAR"
                    self.stdout.write(f'✅ {status}: {product.title} - ${product.price}')
                    created_count += 1
                    
                except Exception as e:
                    self.stdout.write(f'⚠️ Image error for {product.title}: {str(e)}')
                    created_count += 1  # Still count as created
                
                # Small delay to be respectful to image service
                time.sleep(0.5)
                
            except Exception as e:
                self.stdout.write(f'❌ Error creating {product_data["title"]}: {str(e)}')
        
        # Print summary
        self.stdout.write(f'\n📊 FASHION STORE SUMMARY:')
        self.stdout.write(f'   👔 Clothing: {clothing.product_set.count()} products')
        self.stdout.write(f'   👟 Footwear: {footwear.product_set.count()} products')
        self.stdout.write(f'   💎 Accessories: {accessories.product_set.count()} products')
        self.stdout.write(f'   📦 Total: {Product.objects.count()} products')
        self.stdout.write(f'   ⭐ Featured: {Product.objects.filter(featured=True).count()} products')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully created {created_count} fashion products!'))
        self.stdout.write(self.style.SUCCESS('🌐 Visit http://127.0.0.1:8000/ to see your fashion store!'))