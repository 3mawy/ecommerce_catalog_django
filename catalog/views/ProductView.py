from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from catalog.filters import ProductFilter
from catalog.models import Product
from catalog.serializers import ProductIndexSerializer, ProductDetailSerializer
from catalog.serializers.ProductSerializer import ProductCreateUpdateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductIndexSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return super().get_serializer_class()
