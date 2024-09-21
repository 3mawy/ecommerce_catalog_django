from rest_framework import serializers
from catalog.models import ProductType, Category, ProductVariation, Attribute, ProductImage, ProductAttribute


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name']


class AttributeSerializer(serializers.ModelSerializer):
    product_types = ProductTypeSerializer(many=True, read_only=True)  # Adjust the field name accordingly

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'data_type', 'choices', 'product_types']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'slug', 'thumbnail', 'display_order', 'product_type']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_thumbnail', 'is_primary', 'uploaded_at']


class ProductVariationSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(read_only=True)

    class Meta:
        model = ProductVariation
        fields = ['id', 'name', 'price', 'stock', 'attributes', 'image']


