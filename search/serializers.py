from rest_framework import serializers
from catalog.models import Product, ProductVariation


class ProductVariationAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['name']


class ProductAutocompleteSerializer(serializers.ModelSerializer):
    variations = ProductVariationAutocompleteSerializer(many=True, read_only=True)  # Include variations in the response

    class Meta:
        model = Product
        fields = ['id', 'name', 'variations']
