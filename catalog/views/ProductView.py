import json

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from catalog.filters import ProductFilter
from catalog.models import Product
from catalog.serializers import ProductIndexSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer
# from search.documents import ProductDocument


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductIndexSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'name']

    # filterset_class = ProductFilter  # Old filtering logic, non-Elasticsearch filtering

    # TODO:filter by attributes for variations with elasticsearch like the old search
    # def get_queryset(self):
    #     search_term = self.request.query_params.get('search', '')
    #     product_type = self.request.query_params.get('product_type', None)
    #     category_ids = self.request.query_params.get('categories', None)
    #     price_min = self.request.query_params.get('price_min', None)
    #     price_max = self.request.query_params.get('price_max', None)
    #     is_active = self.request.query_params.get('is_active', None)
    #     attributes_str = self.request.query_params.get('attributes', '{}')
    #     attributes = json.loads(attributes_str)
    #
    #     search = ProductDocument.search()
    #
    #     if search_term:
    #         search = search.query('multi_match', query=search_term, fields=['name', 'description'])
    #
    #     if product_type:
    #         search = search.filter('term', product_type=int(product_type))
    #
    #     if category_ids:
    #         search = search.filter('terms', categories=[int(cat_id) for cat_id in category_ids.split(',')])
    #
    #     if price_min or price_max:
    #         range_filter = {}
    #         if price_min:
    #             range_filter['gte'] = price_min
    #         if price_max:
    #             range_filter['lte'] = price_max
    #         search = search.filter('range', price=range_filter)
    #
    #     if is_active is not None:
    #         search = search.filter('term', is_active=is_active.lower() == 'true')
    #
    #     if attributes:
    #         must_queries = []
    #         for attr_name, attr_values in attributes.items():
    #             # Convert all attribute values to lowercase for consistency
    #             attr_values = [str(v).lower() for v in attr_values]
    #             must_queries.append({
    #                 'nested': {
    #                     'path': 'attributes',
    #                     'query': {
    #                         'bool': {
    #                             'must': [
    #                                 {'term': {'attributes.attr_name': attr_name.lower()}},
    #                                 {'terms': {'attributes.attr_value': attr_values}}
    #                             ]
    #                         }
    #                     }
    #                 }
    #             })
    #         search = search.query('bool', must=must_queries)
    #     # TODO: right now we are handling the complix filtering and searching on elastic search but we are still getting the data from the db by id directly
    #     # TODO: so it actually lowers the performance hit on the db but we can still make it better
    #     # TODO: by making the index get the data directly from elastic and the detailed view would get the data from the db
    #     # TODO: i need to handle pagination for elastic search now currently pagination is broken
    #
    #     search_results = search.execute()
    #     product_ids = [hit.meta.id for hit in search_results]
    #     return super().get_queryset().filter(id__in=product_ids)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductIndexSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return super().get_serializer_class()
