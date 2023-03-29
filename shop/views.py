from rest_framework.generics import ListAPIView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoriesList(ListAPIView):
    queryset = Category.objects.filter(
        parent__isnull=True).prefetch_related('subcategories').all()
    serializer_class = CategorySerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.select_related(
        'seller', 'brand', 'category').prefetch_related('images').all()
    serializer_class = ProductSerializer
