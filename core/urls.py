from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='core.index'),
    path('avalanche/product/<slug:slug>/', views.product_detail, name='core.product_detail'),
    path('category/<slug:brand_slug>/<slug:category_slug>/', views.category_detail, name='core.category_detail'),
]