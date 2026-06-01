from collections import defaultdict
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import Brand, Product

# Create your views here.

from django.db.models import Q
from django.shortcuts import render
from .models import Brand, Product  # Adjust imports based on your model structure

def index(request):
    template_data = {'title': 'Avalanche | Luxury Streetwear'}
    categories = ['hoodie', 'joggers', 'shirts', 'jeans', 'bags', 'footwear']
    category_labels = {
        'hoodie': 'Hoodies',
        'joggers': 'Joggers',
        'shirts': 'Shirts',
        'jeans': 'Jeans',
        'bags': 'Bags',
        'footwear': 'Footwear',
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
            display_products = products_by_category[cat][:4]
            total_count = len(products_by_category[cat])

            categories_data.append({
                'key': cat,
                'label': category_labels[cat],
                'products': display_products,
                'total_count': total_count,
            })

        brands_data.append({
            'brand': brand,
            'categories': categories_data,
        })

    return render(request, 'core/index.html', {
        'template_data': template_data,
        'brands_data': brands_data,
    })

def search(request):
    query = request.GET.get('q', '').strip()
    template_data = {'title': f'Search Results for "{query}" | Avalanche'}
    
    categories = ['hoodie', 'joggers', 'shirts', 'jeans', 'bags', 'footwear']
    category_labels = {
        'hoodie': 'Hoodies',
        'joggers': 'Joggers',
        'shirts': 'Shirts',
        'jeans': 'Jeans',
        'bags': 'Bags',
        'footwear': 'Footwear',
    }
    
    search_results = []
    if query:
        # Search across brands and products
        brands = Brand.objects.filter(
            Q(name__icontains=query)
        ).prefetch_related('products')
        
        # Search products
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        ).select_related('brand')
        
        # Organize results by brand
        brand_results = {}
        
        # Add brands that match the search
        for brand in brands:
            if brand.id not in brand_results:
                brand_results[brand.id] = {
                    'brand': brand,
                    'products': []
                }
        
        # Add products that match the search
        for product in products:
            if product.brand:
                if product.brand.id not in brand_results:
                    brand_results[product.brand.id] = {
                        'brand': product.brand,
                        'products': []
                    }
                brand_results[product.brand.id]['products'].append(product)
        
        # Convert to list and organize by category
        for brand_data in brand_results.values():
            products_by_category = defaultdict(list)
            for product in brand_data['products']:
                if product.category in categories:
                    products_by_category[product.category].append(product)
            
            categories_data = []
            for cat in categories:
                if products_by_category[cat]:  # Only show categories with results
                    categories_data.append({
                        'key': cat,
                        'label': category_labels[cat],
                        'products': products_by_category[cat],
                        'total_count': len(products_by_category[cat]),
                    })
            
            if categories_data:  # Only add brand if it has products in valid categories
                search_results.append({
                    'brand': brand_data['brand'],
                    'categories': categories_data,
                })
    
    return render(request, 'core/search_results.html', {
        'template_data': template_data,
        'search_query': query,
        'search_results': search_results,
        'has_results': len(search_results) > 0,
    })

def product_detail(request, brand_slug=None, category_slug=None, product_slug=None, slug=None):
    """Flexible product detail view that works with or without brand/category"""
    
    # Handle direct product access
    if slug:
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
    # Handle full URL with brand and category
    elif product_slug:
        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
    else:
        raise Http404("Invalid product URL")
    
    template_data = {'title': f'{product.name} | Avalanche'}
    
    # Get brand and category info
    brand = product.brand
    category = product.category
    
    # Get category display name
    category_labels = {
        'hoodie': 'Hoodies',
        'joggers': 'Joggers',
        'shirts': 'Shirts',
        'jeans': 'Jeans',
        'bags': 'Bags',
        'footwear': 'Footwear',
    }
    category_display = category_labels.get(category, category.capitalize())
    
    # Get related products (same brand and category) - EXCLUDE products without slugs
    related_products = Product.objects.filter(
        brand=brand,
        category=category
    ).exclude(
        id=product.id
    ).exclude(
        slug__isnull=True  # Exclude null slugs
    ).exclude(
        slug__exact=''     # Exclude empty slugs
    )[:4]
    
    return render(request, 'core/product_detail.html', {
        'template_data': template_data,
        'product': product,
        'brand': brand,
        'category': category,
        'category_display': category_display,
        'related_products': related_products,
    })

def product_detail_direct(request, product_slug):
    """View for direct product access without brand/category in URL"""
    try:
        product = Product.objects.get(slug=product_slug)
        template_data = {'title': f'{product.name} | Avalanche'}
        
        # Get brand and category info for navigation
        brand = product.brand
        category = product.category
        
        # Get related products (same brand and category)
        related_products = Product.objects.filter(
            brand=brand,
            category=category
        ).exclude(id=product.id)[:4]
        
        return render(request, 'core/product_detail.html', {
            'template_data': template_data,
            'product': product,
            'brand': brand,
            'category': category,
            'related_products': related_products,
        })
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

def category_detail(request, brand_slug, category_slug):
    """View to display all products in a specific brand and category"""
    
    # Debug: Print what's being received
    print(f"Category detail called with brand_slug: {brand_slug}, category_slug: {category_slug}")
    
    # Get the brand
    try:
        brand = Brand.objects.get(slug=brand_slug)
    except Brand.DoesNotExist:
        raise Http404(f"Brand with slug '{brand_slug}' does not exist")

    # Validate category slug
    valid_categories = ['hoodie', 'joggers', 'shirts', 'jeans', 'bags', 'footwear']
    if category_slug not in valid_categories:
        raise Http404(f"Invalid category: '{category_slug}'")

    # Get category label
    category_labels = {
        'hoodie': 'Hoodies',
        'joggers': 'Joggers',
        'shirts': 'Shirts',
        'jeans': 'Jeans',
        'bags': 'Bags',
        'footwear': 'Footwear',
    }
    category_label = category_labels.get(category_slug, category_slug.capitalize())
    
    # Get all products for this brand and category
    products = Product.objects.filter(
        brand=brand,
        category=category_slug
    ).exclude(
        slug__isnull=True
    ).exclude(
        slug__exact=''
    ).order_by('-created_at')

    # Debug: Check if products exist
    print(f"Found {products.count()} products for brand '{brand.name}' and category '{category_slug}'")

    return render(request, 'core/section.html', {
        'template_data': {
            'title': f"{category_label} | Avalanche",
        },
        'brand': brand,
        'category_name': category_label,
        'category_slug': category_slug,
        'products': products,
    })