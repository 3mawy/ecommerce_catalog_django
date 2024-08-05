from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from catalog.models import Product, ProductType, Category
from catalog.serializers import ProductDetailSerializer


class ProductViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product_type = ProductType.objects.create(name="Electronics")
        cls.category = Category.objects.create(
            name="Gadgets",
            product_type=cls.product_type,
            slug="gadgets"
        )
        cls.product = Product.objects.create(
            name="Smartphone",
            description="Latest model smartphone",
            product_type=cls.product_type,
            sku="SP123",
            price=299.99,
            stock_quantity=100,
            is_active=True,
            weight=0.2,
            length=15.0,
            width=7.0,
            height=0.8
        )
        cls.url = reverse('product-list')
        cls.detail_url = reverse('product-detail', kwargs={'pk': cls.product.id})  # URL for detail, update, and delete

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        response = self.client.get(self.detail_url)
        product = Product.objects.get(id=self.product.id)
        serializer = ProductDetailSerializer(product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_product(self):
        data = {
            "name": "Laptop",
            "description": "High-performance laptop",
            "product_type": self.product_type.id,
            "categories": [self.category.id],
            "sku": "LP456",
            "price": 999.99,
            "stock_quantity": 50,
            "is_active": True,
            "weight": 1.5,
            "length": 35.0,
            "width": 25.0,
            "height": 2.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product(self):
        data = {
            "name": "Updated Smartphone",
            "description": "Updated description",
            "product_type": self.product_type.id,
            "categories": [self.category.id],
            "sku": "SP123",
            "price": 349.99,
            "stock_quantity": 80,
            "is_active": True,
            "weight": 0.3,
            "length": 16.0,
            "width": 7.5,
            "height": 0.9
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal('349.99'))  # Compare with Decimal

    def test_partial_update_product(self):
        data = {
            "price": 279.99,
            "stock_quantity": 90
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal('279.99'))  # Compare with Decimal

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
