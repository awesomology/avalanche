from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='core.index'),
    path('product/<slug:slug>/', views.product_detail, name='core.product_detail'),
]