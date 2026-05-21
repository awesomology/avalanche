from django.shortcuts import get_object_or_404, render
from .models import Product

# Create your views here.

def index(request):
    template_data = {}
    template_data['title'] = 'Avalanche | Luxury Streetwear'
    return render(request, 'core/index.html', {'template_data': template_data})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'core/product_detail.html', {'product': product})