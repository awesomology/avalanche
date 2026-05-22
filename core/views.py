from collections import defaultdict
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
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

    # Get suggestions - products from same category and brand
    # Exclude the current product
    suggestions = Product.objects.filter(
        Q(category=product.category) | Q(brand=product.brand)
    ).exclude(id=product.id).distinct()[:8]

    # If we don't have enough suggestions, get recent products
    if suggestions.count() < 4:
        recent_products = Product.objects.exclude(id=product.id).order_by('-created_at')[:4]
        # Merge and remove duplicates
        suggestions = (suggestions | recent_products).distinct()[:8]

    return render(request, 'core/product_detail.html', {
        'template_data': {
            'title': f"{product.name} | Avalanche",
        },
        'product': product,
        'suggestions': suggestions
    })