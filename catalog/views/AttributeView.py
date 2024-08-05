from rest_framework import generics
from catalog.models import Attribute
from catalog.serializers.CatalogSerializer import AttributeSerializer


class AttributeListView(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    pagination_class = None
    filterset_fields = ['product_types', 'data_type']
