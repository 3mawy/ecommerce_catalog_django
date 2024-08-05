from rest_framework import generics

from catalog.models import Category
from catalog.serializers import CategorySerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    filterset_fields = ['product_type']