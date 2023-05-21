from django_filters import rest_framework as filters
from .models import Product, Category
from django.shortcuts import get_object_or_404


class ProductsFilter(filters.FilterSet):
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    category = filters.CharFilter(
        field_name='category__slug', method='filter_category')
    brand = filters.CharFilter(field_name='brand__slug', lookup_expr='exact')
    store = filters.CharFilter(field_name='store__slug', lookup_expr='exact')

    def filter_category(self, queryset, name, value):
        category = get_object_or_404(Category, slug=value)
        return queryset.filter(category__in=category.get_descendants(include_self=True))

    class Meta:
        model = Product
        fields = ['category', 'brand', 'store', 'price__gt', 'price__lt']
