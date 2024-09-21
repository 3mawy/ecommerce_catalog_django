from rest_framework import serializers
from catalog.models import Product, ProductAttribute
from catalog.serializers import ProductImageSerializer


class ProductBaseSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'is_active', 'primary_image', 'categories', 'attributes']

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return {
                'url': primary_image.image.url,
                'alt_text': primary_image.alt_text
            }
        return None

    def get_categories(self, obj):
        return [{'id': cat.id, 'name': cat.name, 'slug': cat.slug} for cat in obj.categories.all()]

    def get_attributes(self, obj):
        attributes = ProductAttribute.objects.filter(product=obj)
        # Group attributes by their name
        attributes_by_name = {}
        for attribute in attributes:
            name = attribute.attribute_type.name
            if name not in attributes_by_name:
                attributes_by_name[name] = []
            attributes_by_name[name].append(attribute.value)

        return attributes_by_name


class ProductIndexSerializer(ProductBaseSerializer):
    variations_attributes = serializers.SerializerMethodField()

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + ['variations_attributes']

    # for testing
    def get_variations_attributes(self, obj):
        # Extract and structure attributes from variations
        variations = obj.variations.all()
        variations_attributes = {}
        for variation in variations:
            attributes = variation.attributes  # Assuming attributes is a dict or list
            if isinstance(attributes, dict):
                for name, value in attributes.items():
                    if name not in variations_attributes:
                        variations_attributes[name] = []
                    variations_attributes[name].append(value)
            elif isinstance(attributes, list):
                for attribute in attributes:
                    name = attribute.get('name')
                    value = attribute.get('value')
                    if name not in variations_attributes:
                        variations_attributes[name] = []
                    variations_attributes[name].append(value)

        return variations_attributes


class ProductAttributeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'value']

    def get_name(self, obj):
        return obj.attribute_type.name


class ProductDetailSerializer(ProductBaseSerializer):
    # product_type = ProductTypeSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + ['description', 'product_type', 'created_at', 'updated_at', 'images']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'product_type', 'categories', 'sku', 'price', 'stock',
                  'is_active']
        # You can add custom validation or method fields if needed
