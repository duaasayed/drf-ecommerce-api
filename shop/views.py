from rest_framework.generics import ListAPIView
from .models import Category
from .serializers import CategorySerializer


class CategoriesList(ListAPIView):
    queryset = Category.objects.filter(
        parent__isnull=True).prefetch_related('subcategories').all()
    serializer_class = CategorySerializer
