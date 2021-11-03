import django_filters

from main.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['price', 'category', 'stock_in']
