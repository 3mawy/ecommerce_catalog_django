
from django.db import models
from rest_framework.exceptions import ValidationError


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50, choices=[
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('date', 'Date'),
        ('choice', 'Choice'),
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
    value = models.JSONField()

    def save(self, *args, **kwargs):
        # Ensure the value is processed and stored as a lowercase string
        if self.value:
            if isinstance(self.value, dict) and 'value' in self.value:
                # If the value is a dictionary with a 'value' key, extract and lowercase it
                self.value = self.value['value'].lower()
            elif isinstance(self.value, str):
                # If the value is a string, directly convert it to lowercase
                self.value = self.value.lower()

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        attribute_type = self.attribute_type
        value = self.value
        if attribute_type.data_type == 'integer' and not isinstance(value, int):
            raise ValidationError(f"Value must be an integer for attribute {attribute_type.name}.")
        elif attribute_type.data_type == 'float' and not isinstance(value, float):
            raise ValidationError(f"Value must be a float for attribute {attribute_type.name}.")
        elif attribute_type.data_type == 'boolean' and not isinstance(value, bool):
            raise ValidationError(f"Value must be a boolean for attribute {attribute_type.name}.")
        elif attribute_type.data_type == 'date' and not isinstance(value, str):
            raise ValidationError(f"Value must be a date string for attribute {attribute_type.name}.")
        elif attribute_type.data_type == 'choice' and value not in attribute_type.choices.get('choices', []):
            raise ValidationError(f"Value must be one of the choices for attribute {attribute_type.name}.")
