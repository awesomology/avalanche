from django.urls import path, re_path
from . import views, admin_views, notification_views

urlpatterns = [
    path('', views.index, name='core.index'),
    path('search/', views.search, name='core.search'),
    
    # Category detail - MUST come before product detail patterns
    path('category/<slug:brand_slug>/<slug:category_slug>/', views.category_detail, name='core.category_detail'),
    
    # Direct product access (no brand/category)
    re_path(r'^product/(?P<slug>[\w-]+)/$', views.product_detail, name='core.product_detail_simple'),
    re_path(r'^avalanche/product/(?P<slug>[\w-]+)/$', views.product_detail, name='core.product_detail_avalanche'),
    path('product/<slug:product_slug>/', views.product_detail_direct, name='core.product_detail_direct'),
    
    # Product detail with brand and category - this should be LAST
    path('<slug:brand_slug>/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='core.product_detail'),

    # Admin custom views
    path('admins/manage-featured-products/', admin_views.manage_featured_products, name='core.manage_featured_products'),

    # Silent notification endpoint
    path('api/notify-purchase-intent/', notification_views.notify_purchase_intent, name='notify_purchase_intent'),

    #DEBUGGING ENDPOINTS - REMOVE IN PRODUCTION
    path('test-email/', views.test_email, name='test_email'),
]