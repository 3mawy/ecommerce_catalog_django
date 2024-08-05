from rest_framework import serializers
from catalog.models import Product, ProductAttribute
from catalog.serializers import ProductImageSerializer
from catalog.serializers.CatalogSerializer import ProductAttributeSerializer, ProductVariationSerializer


class ProductBaseSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock_quantity', 'is_active', 'primary_image', 'categories',
                  'attributes']

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
        # Fetch attributes for the product
        attributes = ProductAttribute.objects.filter(product=obj)
        # Serialize them using ProductAttributeSerializer
        serializer = ProductAttributeSerializer(attributes, many=True)
        return serializer.data


class ProductIndexSerializer(ProductBaseSerializer):
    variations_attributes = serializers.SerializerMethodField()  # New field

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + ['variations_attributes']

    def get_variations_attributes(self, obj):
        # Extract attributes from variations
        variations = obj.variations.all()
        attributes_list = []
        for variation in variations:
            if variation.attributes:
                attributes_list.append(variation.attributes)
        return attributes_list


class ProductDetailSerializer(ProductBaseSerializer):
    # product_type = ProductTypeSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + ['description', 'product_type', 'weight', 'length', 'width',
                                                      'height', 'created_at', 'updated_at', 'images']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'product_type', 'categories', 'sku', 'price', 'stock_quantity',
                  'is_active', 'weight', 'length', 'width', 'height']
        # You can add custom validation or method fields if needed
