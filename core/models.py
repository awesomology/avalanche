from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

CATEGORY_CHOICES = [
    ('hoodie', 'Hoodies'),
    ('joggers', 'Joggers'),
    ('shirts', 'Shirts'),
    ('jeans', 'Jeans'),
    ('bags', 'Bags'),
    ('footwear', 'Footwear'),
]

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    is_active = models.BooleanField(default=True)  # Option to hide brand
    order = models.IntegerField(default=0, help_text="Order in which brands appear on front page")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:110] or 'brand'
            slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order', 'name']  # Brands will be ordered by 'order' first, then by name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='shirts')
    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products'
    )
    image_url = models.ImageField(upload_to='products/', blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show on front page")
    featured_order = models.IntegerField(default=0, help_text="Order on front page (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':  # Check for empty string too
            base_slug = slugify(self.name)[:110] or 'product'
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Generate the correct URL for this product"""
        if self.brand and self.category:
            return reverse('core.product_detail', kwargs={
                'brand_slug': self.brand.slug,
                'category_slug': self.category,
                'product_slug': self.slug
            })
        # Fallback for products without brand
        return reverse('core.product_detail_direct', kwargs={'product_slug': self.slug})

    def __str__(self):
        return self.name + ' - ₦' + str(self.price) + ' - ' + self.category + self.slug
    
    class Meta:
        ordering = ['featured_order', '-created_at']

class FeaturedSection(models.Model):
    """Optional: Create custom featured sections"""
    SECTION_TYPES = [
        ('brand_spotlight', 'Brand Spotlight'),
        ('new_arrivals', 'New Arrivals'),
        ('trending', 'Trending'),
        ('custom', 'Custom Section'),
    ]
    
    title = models.CharField(max_length=200)
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES, default='brand_spotlight')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    max_products = models.IntegerField(default=8, help_text="Maximum number of products to show")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']