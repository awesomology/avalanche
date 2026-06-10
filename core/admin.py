from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Product, FeaturedSection

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'product_count']
    list_editable = ['is_active', 'order']
    search_fields = ['name']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Number of Products'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'brand', 'category', 'price', 'is_featured', 'featured_order', 'image_preview']
    list_editable = ['is_featured', 'featured_order', 'price']
    list_filter = ['category', 'brand', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image_url.url)
        return "No Image"
    image_preview.short_description = 'Image'


class FeaturedSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'section_type', 'is_active', 'order', 'max_products']
    list_editable = ['is_active', 'order', 'max_products']
    list_filter = ['section_type', 'is_active']


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(FeaturedSection, FeaturedSectionAdmin)