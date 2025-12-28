from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Create basic categories'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and apparel items'},
            {'name': 'Footwear', 'slug': 'footwear', 'description': 'Shoes and footwear'},
            {'name': 'Accessories', 'slug': 'accessories', 'description': 'Fashion accessories, jewelry, watches, and more'},
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                # Update existing category
                category.name = cat_data['name']
                category.description = cat_data['description']
                category.save()
                self.stdout.write(f'Updated category: {category.name}')
        
        self.stdout.write(self.style.SUCCESS('Categories ready!'))