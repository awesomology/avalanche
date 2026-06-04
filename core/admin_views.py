from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from .models import Brand, Product


@staff_member_required
def manage_featured_products(request):
    """Custom admin view to easily manage featured products"""
    brands = Brand.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Clear existing featured products
        Product.objects.filter(is_featured=True).update(is_featured=False, featured_order=0)
        
        # Set new featured products
        featured_count = 0
        for brand in brands:
            product_ids = request.POST.getlist(f'products_{brand.id}')
            for order, product_id in enumerate(product_ids):
                try:
                    product = Product.objects.get(id=product_id)
                    product.is_featured = True
                    product.featured_order = featured_count
                    product.save()
                    featured_count += 1
                except Product.DoesNotExist:
                    pass
        
        messages.success(request, f'Successfully updated {featured_count} featured products!')
        return redirect('core.manage_featured_products')
    
    context = {
        'brands': brands,
        'title': 'Manage Featured Products',
    }
    return render(request, 'admin/manage_featured_products.html', context)