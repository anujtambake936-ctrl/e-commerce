import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eCommerce.settings')
django.setup()

from products.models import Product, Category

# Clear existing products
Product.objects.all().delete()
print("Cleared existing products")

# Create categories
clothing, _ = Category.objects.get_or_create(
    name='Clothing',
    defaults={'slug': 'clothing', 'description': 'Fashion and apparel items'}
)
footwear, _ = Category.objects.get_or_create(
    name='Footwear', 
    defaults={'slug': 'footwear', 'description': 'Shoes and footwear'}
)
accessories, _ = Category.objects.get_or_create(
    name='Accessories',
    defaults={'slug': 'accessories', 'description': 'Fashion accessories and jewelry'}
)

# Fashion products
products = [
    # Clothing
    {
        'title': 'Classic White T-Shirt',
        'price': 29.99,
        'description': 'Premium cotton t-shirt with comfortable fit. Perfect for everyday wear with soft fabric and durable construction.',
        'category': clothing,
        'brand': 'EssentialWear'
    },
    {
        'title': 'Vintage Denim Jacket',
        'price': 89.99,
        'description': 'Classic blue denim jacket with vintage wash and authentic styling. A timeless piece for any wardrobe.',
        'category': clothing,
        'brand': 'VintageStyle'
    },
    {
        'title': 'Cozy Knit Sweater',
        'price': 69.99,
        'description': 'Soft knit sweater perfect for cooler weather. Made with premium wool blend for warmth and comfort.',
        'category': clothing,
        'brand': 'CozyKnits'
    },
    {
        'title': 'Elegant Black Dress',
        'price': 129.99,
        'description': 'Sophisticated black dress perfect for formal occasions. Features elegant silhouette and premium fabric.',
        'category': clothing,
        'brand': 'ElegantStyle'
    },
    {
        'title': 'Casual Button-Down Shirt',
        'price': 49.99,
        'description': 'Versatile button-down shirt suitable for work or casual wear. Made with breathable cotton fabric.',
        'category': clothing,
        'brand': 'CasualFit'
    },
    {
        'title': 'Slim Fit Dark Jeans',
        'price': 79.99,
        'description': 'Modern slim fit jeans in dark wash. Features stretch denim for comfort and contemporary styling.',
        'category': clothing,
        'brand': 'ModernDenim'
    },
    
    # Footwear
    {
        'title': 'Premium Running Sneakers',
        'price': 119.99,
        'description': 'High-performance running sneakers with advanced cushioning and breathable mesh upper for optimal comfort.',
        'category': footwear,
        'brand': 'SportTech'
    },
    {
        'title': 'Classic Leather Boots',
        'price': 159.99,
        'description': 'Handcrafted leather boots with durable construction. Perfect for both casual and semi-formal occasions.',
        'category': footwear,
        'brand': 'LeatherCraft'
    },
    {
        'title': 'White Canvas Sneakers',
        'price': 59.99,
        'description': 'Timeless white canvas sneakers with rubber sole. A versatile choice for casual everyday wear.',
        'category': footwear,
        'brand': 'ClassicStep'
    },
    {
        'title': 'Formal Oxford Shoes',
        'price': 189.99,
        'description': 'Elegant oxford shoes in genuine leather. Perfect for business meetings and formal events.',
        'category': footwear,
        'brand': 'FormalStep'
    },
    
    # Accessories
    {
        'title': 'Luxury Stainless Steel Watch',
        'price': 249.99,
        'description': 'Premium stainless steel watch with sapphire crystal and water resistance. Elegant design for any occasion.',
        'category': accessories,
        'brand': 'TimeClassic'
    },
    {
        'title': 'Genuine Leather Wallet',
        'price': 69.99,
        'description': 'Handcrafted leather wallet with multiple card slots and bill compartment. Compact yet functional design.',
        'category': accessories,
        'brand': 'LeatherGoods'
    },
    {
        'title': 'Designer Sunglasses',
        'price': 129.99,
        'description': 'Stylish sunglasses with UV protection and polarized lenses. Modern frame design with premium materials.',
        'category': accessories,
        'brand': 'SunStyle'
    },
    {
        'title': 'Sterling Silver Bracelet',
        'price': 99.99,
        'description': 'Elegant sterling silver chain bracelet with polished finish. Perfect for everyday wear or special occasions.',
        'category': accessories,
        'brand': 'SilverCraft'
    },
    {
        'title': 'Premium Leather Belt',
        'price': 59.99,
        'description': 'High-quality leather belt with classic buckle design. Essential accessory for any professional wardrobe.',
        'category': accessories,
        'brand': 'BeltCraft'
    },
    {
        'title': 'Stylish Baseball Cap',
        'price': 34.99,
        'description': 'Adjustable baseball cap with embroidered logo and curved brim. Perfect for casual outings and sports.',
        'category': accessories,
        'brand': 'CapStyle'
    },
]

# Create products
for product_data in products:
    product = Product.objects.create(
        title=product_data['title'],
        category=product_data['category'],
        brand=product_data['brand'],
        price=product_data['price'],
        description=product_data['description'],
        featured=product_data['price'] > 100,
        active=True
    )
    print(f'✓ Created: {product.title}')

# Print summary
print(f"\n=== SUMMARY ===")
print(f"Clothing: {clothing.product_set.count()} products")
print(f"Footwear: {footwear.product_set.count()} products") 
print(f"Accessories: {accessories.product_set.count()} products")
print(f"Total: {Product.objects.count()} products")
print("✓ Fashion products created successfully!")