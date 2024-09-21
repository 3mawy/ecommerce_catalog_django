from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    attributes = models.ManyToManyField('Attribute', blank=True, related_name='product_types')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', blank=True)
    sku = models.CharField(max_length=64, unique=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_stock(self):
        if not self.variations.exists():
            return self.stock
        # Total stock based on variations
        return sum(variation.stock for variation in self.variations.all())

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['product_type']),
            models.Index(fields=['product_type', 'price']),
        ]


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=64, unique=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    attributes = models.JSONField(default=dict)  # Variant level attributes
    image = models.ForeignKey('ProductImage', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure attributes keys and values are in lowercase
        if self.attributes:
            processed_attributes = {}
            for key, value in self.attributes.items():
                key = key.lower()
                processed_attributes[key] = str(value).lower()
            self.attributes = processed_attributes
        else:
            self.attributes = {}
        super().save(*args, **kwargs)

    def get_price(self):
        return self.price if self.price is not None else self.product.price

    def get_sku(self):
        return self.sku if self.sku is not None else self.product.sku

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    class Meta:
        indexes = [
            models.Index(fields=['product']),
        ]
