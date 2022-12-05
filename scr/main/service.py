import django_filters
from rest_framework import viewsets

from .models import Product


class ProductFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['price', 'category', 'stock_in']


class BaseModelViewSet(viewsets.ModelViewSet):
    """Mixin to define update and create objects hooks"""

    search_fields = ['name']
    lookup_field = 'slug'

    def perform_create(self, serializer):
        product = serializer.save()
        product.slug = product.name
        product.save()

    def perform_update(self, serializer):
        product = serializer.save()
        product.slug = product.name
        product.save()
