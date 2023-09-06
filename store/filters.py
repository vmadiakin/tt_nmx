from django_filters import rest_framework as filters
from store.models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    category_id = filters.NumberFilter(field_name='category__id')
    category_name = filters.CharFilter(field_name='category__name',
                                       lookup_expr='icontains')
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ('name', 'category_id', 'category_name', 'price', 'is_published', 'is_deleted')
