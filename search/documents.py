from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from catalog.models import Product, ProductVariation, ProductAttribute

# Define the Elasticsearch index
product_index = Index('products')

@registry.register_document
class ProductDocument(Document):
    name = fields.TextField(
        analyzer="edge_ngram_analyzer",
        search_analyzer="standard"
    )

    attributes = fields.NestedField(properties={
        'attr_name': fields.KeywordField(),
        'attr_value': fields.KeywordField(),
    })

    variations = fields.NestedField(properties={
        'name': fields.TextField(),
    })
    images = fields.TextField(multi=True)
    categories = fields.IntegerField(multi=True)
    product_type = fields.IntegerField()

    class Django:
        model = Product
        fields = [
            'description',
            'price',
            'is_active',
        ]
        filter_fields = {
            'categories': 'terms',
            'product_type': 'exact',
            'price': 'range',
            'is_active': 'exact',
            'attributes': 'nested',  # Ensure attributes are treated as nested
            'variations': 'nested',  # Ensure variations are treated as nested
        }
        ignore_signals = False

    class Index:
        name = 'products'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "edge_ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "edge_ngram_tokenizer",
                        "filter": ["lowercase"]
                    }
                },
                "tokenizer": {
                    "edge_ngram_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 3,
                        "max_gram": 20,
                        "token_chars": ["letter", "digit"]
                    }
                }
            }
        }

    def prepare_product_type(self, instance):
        return instance.product_type.id if instance.product_type else None

    def prepare_categories(self, instance):
        return [category.id for category in instance.categories.all()]

    # TODO: FIX THIS SHIT
    def prepare_images(self, instance):
        # Correctly access the 'url' of the ImageField
        return [image.image.url for image in instance.images.all()]

    def prepare_attributes(self, instance):
        attributes = []
        for attr in instance.attributes.all():
            attr_name = attr.attribute_type.name.lower()  # Ensure attribute name is in lowercase
            attr_value = attr.value
            print(attr_name)
            print(attr_value)
            if isinstance(attr_value, str):
                attr_value = attr_value.lower()  # Ensure string values are in lowercase
            elif isinstance(attr_value, float):
                attr_value = str(attr_value).lower()  # Convert float to lowercase string
            elif isinstance(attr_value, list):
                # Ensure each list item is a lowercase string
                attr_value = [str(v).lower() if isinstance(v, str) else str(v) for v in attr_value]
            elif isinstance(attr_value, bool):
                attr_value = str(attr_value).lower()  # Convert boolean to lowercase string

            attributes.append({
                'attr_name': attr_name,
                'attr_value': attr_value  # Use the processed value
            })

        return attributes

    def prepare_variations(self, instance):
        return [{'name': variation.name} for variation in instance.variations.all()]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, ProductAttribute):
            return related_instance.product
        elif isinstance(related_instance, ProductVariation):
            return related_instance.product
        return super().get_instances_from_related(related_instance)
