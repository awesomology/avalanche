from collections import defaultdict
from django.shortcuts import get_object_or_404, render
from .models import Brand, Product

# Create your views here.

def index(request):
    template_data = {'title': 'Avalanche | Luxury Streetwear'}
    categories = ['hoodie', 'joggers', 'shirts', 'jeans', 'bags', 'shoes']
    category_labels = {
        'hoodie': 'Hoodies',
        'joggers': 'Joggers',
        'shirts': 'Shirts',
        'jeans': 'Jeans',
        'bags': 'Bags',
        'shoes': 'Shoes',
    }

    brands = Brand.objects.prefetch_related('products')
    brands_data = []
    for brand in brands:
        products_by_category = defaultdict(list)
        for product in brand.products.all():
            if product.category in categories:
                products_by_category[product.category].append(product)

        categories_data = []
        for cat in categories:
            categories_data.append({
                'key': cat,
                'label': category_labels[cat],
                'products': products_by_category[cat],
            })

        brands_data.append({
            'brand': brand,
            'categories': categories_data,
        })

    return render(request, 'core/index.html', {
        'template_data': template_data,
        'brands_data': brands_data,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'core/product_detail.html', {'product': product})