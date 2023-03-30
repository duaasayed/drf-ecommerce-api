from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Category, Product, Brand, Seller
from . import serializers
from .pagination import ProductsPaginator
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductsFilter


class CategoriesList(ListAPIView):
    queryset = Category.objects.filter(
        parent__isnull=True).prefetch_related('subcategories').all()
    serializer_class = serializers.CategorySerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.select_related(
        'seller', 'brand', 'category').prefetch_related('images').all()
    serializer_class = serializers.ProductSerializer
    pagination_class = ProductsPaginator
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['published_at', 'price']
    filterset_class = ProductsFilter


class BrandDetails(RetrieveAPIView):
    queryset = Brand.objects.prefetch_related(
        'products__category', 'products__seller').all()
    serializer_class = serializers.BrandDetailsSerializer
    lookup_field = 'slug'


class SellerDetails(RetrieveAPIView):
    queryset = Seller.objects.prefetch_related(
        'products__category', 'products__brand').all()
    serializer_class = serializers.SellerDetailsSerializer
    lookup_field = 'slug'


class CategoryDetails(RetrieveAPIView):
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = serializers.CategoryDetailsSerializer
    lookup_field = 'slug'


class ProductDetails(RetrieveAPIView):
    queryset = Product.objects.select_related(
        'brand', 'category', 'seller').prefetch_related('images').all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'
