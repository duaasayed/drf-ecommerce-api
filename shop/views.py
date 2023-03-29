from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Category, Product, Brand
from .serializers import CategorySerializer, ProductSerializer, BrandDetailsSerializer
from .pagination import ProductsPaginator
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductsFilter


class CategoriesList(ListAPIView):
    queryset = Category.objects.filter(
        parent__isnull=True).prefetch_related('subcategories').all()
    serializer_class = CategorySerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.select_related(
        'seller', 'brand', 'category').prefetch_related('images').all()
    serializer_class = ProductSerializer
    pagination_class = ProductsPaginator
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['published_at', 'price']
    filterset_class = ProductsFilter


class BrandDetails(RetrieveAPIView):
    queryset = Brand.objects.prefetch_related(
        'products__category', 'products__seller').all()
    serializer_class = BrandDetailsSerializer
    lookup_field = 'slug'
