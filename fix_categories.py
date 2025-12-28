import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eCommerce.settings')
django.setup()

from products.models import Product, Category

# Get or create categories
clothing, _ = Category.objects.get_or_create(name='Clothing')
footwear, _ = Category.objects.get_or_create(name='Footwear') 
accessories, _ = Category.objects.get_or_create(name='Accessories')

# Assign products to categories based on their titles/descriptions
for product in Product.objects.all():
    title_lower = product.title.lower()
    desc_lower = product.description.lower()
    
    if any(word in title_lower or word in desc_lower for word in ['shirt', 'jacket', 'coat', 'clothing', 'cotton', 'casual']):
        product.category = clothing
    elif any(word in title_lower or word in desc_lower for word in ['shoe', 'boot', 'sneaker', 'footwear']):
        product.category = footwear
    else:
        product.category = accessories
    
    product.save()
    print(f"Assigned {product.title} to {product.category.name}")

print(f"\nFinal counts:")
print(f"Clothing: {clothing.product_set.count()}")
print(f"Footwear: {footwear.product_set.count()}")
print(f"Accessories: {accessories.product_set.count()}")