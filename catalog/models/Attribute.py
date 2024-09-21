
from django.db import models
from rest_framework.exceptions import ValidationError

from catalog.models import ProductType


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50, choices=[
        ('string', 'String'),
        ('number', 'Number'),
        ('boolean', 'Boolean'),
        ('date', 'Date'),
    ])
    choices = models.JSONField(blank=True, null=True)  # For choice attributes

    def save(self, *args, **kwargs):
        # Convert name to lowercase before saving
        if self.name:
            self.name = self.name.lower()

        # Ensure that all keys and values in choices are lowercase
        if self.choices and isinstance(self.choices, dict):
            self.choices = {
                key.lower(): [
                    val.lower() if isinstance(val, str) else val
                    for val in values
                ]
                for key, values in self.choices.items()
            }

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='attributes')
    attribute_type = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Ensure the value is processed and stored as a lowercase string
        if self.value:
            self.value = str(self.value).lower()

        super().save(*args, **kwargs)

