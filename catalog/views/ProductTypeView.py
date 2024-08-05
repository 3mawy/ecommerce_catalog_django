from rest_framework import generics

from catalog.models import ProductType
from catalog.serializers import ProductTypeSerializer


class ProductTypeListView(generics.ListCreateAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    pagination_class = None