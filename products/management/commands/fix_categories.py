from django.core.management.base import BaseCommand
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Fix product categories based on their content'

    def handle(self, *args, **options):
        self.stdout.write('Fixing product categories...')
        
        # Get or create categories
        clothing, _ = Category.objects.get_or_create(name='Clothing')
        footwear, _ = Category.objects.get_or_create(name='Footwear') 
        accessories, _ = Category.objects.get_or_create(name='Accessories')
        
        # Define category keywords
        clothing_keywords = [
            'shirt', 'jacket', 'coat', 'hoodie', 'sweater', 'dress', 'pants', 'jeans',
            'shorts', 'skirt', 'blouse', 'top', 'tee', 't-shirt', 'clothing', 'cotton',
            'casual', 'formal', 'winter', 'summer', 'sleeve', 'collar', 'fabric',
            'mens', 'womens', 'unisex', 'fit', 'slim', 'regular', 'oversized'
        ]
        
        footwear_keywords = [
            'shoe', 'shoes', 'boot', 'boots', 'sneaker', 'sneakers', 'sandal', 'sandals',
            'heel', 'heels', 'loafer', 'loafers', 'oxford', 'running', 'walking',
            'athletic', 'sport', 'casual', 'formal', 'leather', 'canvas', 'rubber',
            'sole', 'lace', 'slip-on', 'high-top', 'low-top'
        ]
        
        accessories_keywords = [
            'watch', 'watches', 'bracelet', 'necklace', 'ring', 'earring', 'jewelry',
            'belt', 'belts', 'bag', 'bags', 'wallet', 'purse', 'sunglasses', 'glasses',
            'specs', 'spectacles', 'hat', 'cap', 'scarf', 'gloves', 'tie', 'bow tie',
            'cufflinks', 'chain', 'pendant', 'charm', 'brooch', 'pin', 'keychain',
            'wristband', 'band', 'strap', 'gold', 'silver', 'diamond', 'pearl',
            'leather', 'metal', 'stainless', 'steel', 'crystal'
        ]
        
        # Categorize products
        for product in Product.objects.all():
            title_lower = product.title.lower()
            desc_lower = product.description.lower()
            combined_text = f"{title_lower} {desc_lower}"
            
            # Count matches for each category
            clothing_matches = sum(1 for keyword in clothing_keywords if keyword in combined_text)
            footwear_matches = sum(1 for keyword in footwear_keywords if keyword in combined_text)
            accessories_matches = sum(1 for keyword in accessories_keywords if keyword in combined_text)
            
            # Assign to category with most matches
            if footwear_matches > clothing_matches and footwear_matches > accessories_matches:
                product.category = footwear
                category_name = "Footwear"
            elif accessories_matches > clothing_matches and accessories_matches > footwear_matches:
                product.category = accessories
                category_name = "Accessories"
            else:
                product.category = clothing
                category_name = "Clothing"
            
            product.save()
            self.stdout.write(f"Assigned '{product.title}' to {category_name}")
        
        # Print final counts
        self.stdout.write(f"\nFinal category counts:")
        self.stdout.write(f"Clothing: {clothing.product_set.count()} products")
        self.stdout.write(f"Footwear: {footwear.product_set.count()} products")
        self.stdout.write(f"Accessories: {accessories.product_set.count()} products")
        
        self.stdout.write(self.style.SUCCESS('Successfully fixed product categories!'))