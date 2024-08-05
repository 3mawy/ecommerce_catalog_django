import json
import logging

import django_filters
from django.db.models import Subquery, Q
from django_filters import rest_framework as filters
from catalog.models import Category, ProductType, Product, ProductVariation

logger = logging.getLogger(__name__)


class ProductFilter(filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    categories = filters.CharFilter(method='filter_categories')

    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    attributes = django_filters.CharFilter(method='filter_by_attribute')

    class Meta:
        model = Product
        fields = ['categories', 'product_type', 'price', 'is_active']

    def filter_search(self, queryset, name, value):
        """
        Custom filter method to handle search in product fields and attributes.
        """
        if value:
            value_lower = value.lower()

            # Subquery for finding Product IDs with matching attributes
            product_attributes_subquery = Product.objects.filter(
                attributes__value__icontains=value_lower
            ).values('id')

            # # Subquery for finding Product IDs with matching ProductVariation attributes
            # product_variations_subquery = ProductVariation.objects.filter(
            #     RawSQL("attributes::jsonb ? %s", (value,))
            # ).values('product_id')

            # Subquery for finding ProductVariation IDs with matching name
            product_variation_name_subquery = ProductVariation.objects.filter(
                name__icontains=value
            ).values('id')

            queryset = queryset.filter(
                Q(name__icontains=value) |
                Q(description__icontains=value) |
                Q(id__in=Subquery(product_attributes_subquery)) |
                # Q(id__in=Subquery(product_variations_subquery)) |
                Q(id__in=Subquery(product_variation_name_subquery))
            ).distinct()

        return queryset

    from django.db.models import Q
    import json

    def filter_by_attribute(self, queryset, name, value):
        query = Q()

        # Convert the JSON string value into a dictionary
        try:
            attributes = json.loads(value)
        except json.JSONDecodeError:
            # Handle JSON parsing error
            return queryset

        for attr_name, attr_values in attributes.items():
            attr_name_lower = attr_name.lower()

            if isinstance(attr_values, list):

                for attr_value in attr_values:
                    if isinstance(attr_value, bool):
                        query |= Q(attributes__attribute_type__name=attr_name_lower,
                                   attributes__value__contains=attr_value)
                        query |= Q(variations__attributes__contains={attr_name_lower: attr_value})
                    else:
                        attr_value_lower = attr_value.lower() if isinstance(attr_value, str) else attr_value
                        if attr_value_lower == "true":
                            attr_value_lower = True
                        elif attr_value_lower == "false":
                            attr_value_lower = False
                        query |= Q(attributes__attribute_type__name=attr_name_lower,
                                   attributes__value__contains=attr_value_lower)
                        query |= Q(variations__attributes__contains={attr_name_lower: attr_value_lower})
            # elif isinstance(attr_values, str):
            #     attr_value_lower = attr_values.lower()
            #     query |= Q(attributes__attribute_type__name=attr_name_lower,
            #                attributes__value__contains={attr_name_lower: attr_value_lower})
            # else:
            #     query |= Q(attributes__attribute_type__name=attr_name_lower,
            #                attributes__value__contains={attr_name_lower: attr_values})

        return queryset.filter(query).distinct()

    def filter_categories(self, queryset, name, value):
        if value:
            category_ids = [int(cat_id) for cat_id in value.split(',') if cat_id.isdigit()]

            if category_ids:
                queryset = queryset.filter(categories__id__in=category_ids)

        return queryset
