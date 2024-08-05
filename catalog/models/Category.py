from django.db import models

from catalog.models import ProductType


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='category_thumbnails/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
