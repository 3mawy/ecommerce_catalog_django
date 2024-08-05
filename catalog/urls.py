from rest_framework import routers
from django.urls import path, include

from catalog.views.AttributeView import AttributeListView
from catalog.views.CategoryView import CategoryListView
from catalog.views.ProductTypeView import ProductTypeListView
from catalog.views.ProductView import ProductViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('product-types/', ProductTypeListView.as_view(), name='product-type-list'),
    path('attributes/', AttributeListView.as_view(), name='attribute-list'),

]
