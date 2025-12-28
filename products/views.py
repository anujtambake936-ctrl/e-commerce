from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Category
from carts.models import Cart


@method_decorator(login_required, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category
    template_name = "products/category_detail.html"
    context_object_name = 'category'
    
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        
        # Get products for this category using smart filtering
        category = self.get_object()
        all_products = Product.objects.filter(active=True)
        
        if category.name == 'Clothing':
            products = [p for p in all_products if any(word in f"{p.title.lower()} {p.description.lower()}" 
                       for word in ['shirt', 'jacket', 'coat', 'hoodie', 'cotton', 'casual', 'fit', 'sleeve', 'womens', 'mens']) 
                       and 'oxford' not in p.title.lower() and 'swiss automatic watch' not in p.title.lower()]
        elif category.name == 'Footwear':
            products = [p for p in all_products if any(word in f"{p.title.lower()} {p.description.lower()}" 
                       for word in ['shoe', 'boot', 'sneaker', 'footwear', 'running', 'walking']) 
                       and 'necklace' not in p.title.lower()]
        elif category.name == 'Accessories':
            products = [p for p in all_products if (any(word in f"{p.title.lower()} {p.description.lower()}" 
                       for word in ['watch', 'bracelet', 'necklace', 'ring', 'jewelry', 'gold', 'silver', 'chain', 'steel', 'stainless']) 
                       or not any(word in f"{p.title.lower()} {p.description.lower()}" 
                                for word in ['shirt', 'jacket', 'coat', 'hoodie', 'cotton', 'casual', 'fit', 'sleeve', 'womens', 'mens', 'shoe', 'boot', 'sneaker']))
                       and 'swiss automatic watch' not in p.title.lower()]
        else:
            products = all_products
            
        context['products'] = products
        return context


@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        category = self.request.GET.get('category')
        all_products = Product.objects.filter(active=True).order_by('-timestamp')
        
        if category == 'clothing':
            products = [p for p in all_products if any(word in f"{p.title.lower()} {p.description.lower()}" 
                       for word in ['shirt', 'jacket', 'coat', 'hoodie', 'cotton', 'casual', 'fit', 'sleeve', 'womens', 'mens', 'dress', 'jeans', 'pants', 'shorts', 'blouse', 'top', 'tee', 't-shirt', 'clothing', 'fabric']) 
                       and 'oxford' not in p.title.lower() and 'swiss automatic watch' not in p.title.lower()]
            return products
        elif category == 'footwear':
            products = [p for p in all_products if any(word in f"{p.title.lower()} {p.description.lower()}" 
                       for word in ['shoe', 'shoes', 'boot', 'boots', 'sneaker', 'sneakers', 'sandal', 'sandals', 'heel', 'heels', 'loafer', 'loafers', 'oxford', 'running', 'walking', 'athletic', 'sport', 'footwear', 'sole', 'lace']) 
                       and 'necklace' not in p.title.lower()]
            return products
        elif category == 'accessories':
            # Only true fashion accessories - exclude electronics and swiss automatic watch
            products = [p for p in all_products if (any(word in f"{p.title.lower()} {p.description.lower()}" 
                       for word in ['watch', 'watches', 'bracelet', 'necklace', 'ring', 'earring', 'jewelry', 'belt', 'belts', 'bag', 'bags', 'wallet', 'purse', 'sunglasses', 'glasses', 'specs', 'spectacles', 'hat', 'cap', 'scarf', 'gloves', 'tie', 'bow tie', 'cufflinks', 'chain', 'pendant', 'charm', 'brooch', 'pin', 'keychain', 'wristband', 'band', 'strap', 'gold', 'silver', 'diamond', 'pearl']) 
                       and not any(word in f"{p.title.lower()} {p.description.lower()}" 
                                 for word in ['monitor', 'screen', 'display', 'computer', 'gaming', 'laptop', 'desktop', 'electronic', 'digital', 'tech', 'device', 'hardware', 'ssd', 'hard drive', 'usb', 'portable', 'external', 'internal', 'curved', 'lcd', 'led', 'oled', 'qled'])
                       and 'swiss automatic watch' not in p.title.lower())]
            return products
        else:
            return all_products
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['new_products_count'] = Product.objects.new_products().count()
        context['featured_products_count'] = Product.objects.featured().count()
        
        # Add current category for page title
        category = self.request.GET.get('category')
        if category:
            context['current_category'] = category.title()
        
        return context


@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
