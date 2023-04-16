from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Category, Product, Brand, Store, Review, Question, Answer
from . import serializers
from .pagination import ProductsPaginator
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductsFilter
from rest_framework.viewsets import ModelViewSet
from .permissions import ReviewsPermissions, QuestionsPermissions, AnswersPermissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from rest_framework.response import Response


class CategoriesList(ListAPIView):
    queryset = Category.objects.filter(
        parent__isnull=True).prefetch_related('subcategories').all()
    serializer_class = serializers.CategorySerializer


class BestSellersView(ListAPIView):
    queryset = Product.objects.select_related('brand', 'category', 'store')\
        .prefetch_related('images', 'reviews').annotate(order_count=Count('orderproduct'), reviews_count=Count('reviews'))\
        .filter(order_count__gt=0).order_by('-order_count')[:10]
    serializer_class = serializers.ProductSerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.select_related(
        'store', 'brand', 'category').prefetch_related('images', 'reviews')\
        .annotate(reviews_count=Count('reviews')).all()
    serializer_class = serializers.ProductSerializer
    pagination_class = ProductsPaginator
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['published_at', 'price']
    filterset_class = ProductsFilter


class BrandDetails(RetrieveAPIView):
    queryset = Brand.objects.prefetch_related(
        'products__category', 'products__store').all()
    serializer_class = serializers.BrandDetailsSerializer
    lookup_field = 'slug'


class StoreDetails(RetrieveAPIView):
    queryset = Store.objects.prefetch_related(
        'products__category', 'products__brand').all()
    serializer_class = serializers.StoreDetailsSerializer
    lookup_field = 'slug'


class CategoryDetails(RetrieveAPIView):
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = serializers.CategoryDetailsSerializer
    lookup_field = 'slug'


class ProductDetails(RetrieveAPIView):
    queryset = Product.objects.select_related(
        'brand', 'category', 'store').prefetch_related('images').all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = serializers.ProductSerializer(obj)
        related_products = serializers.ProductSerializer(
            obj.related_products, many=True)
        response = {'product': serializer.data,
                    'related_products': related_products.data}
        return Response(response)


class ReviewViewset(ModelViewSet):
    queryset = Review.objects.select_related('customer').all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated, ReviewsPermissions]

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs.get('product_id'))


class QuestionViewset(ModelViewSet):
    queryset = Question.objects.select_related('customer').all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated, QuestionsPermissions]

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs.get('product_id'))


class AnswerViewset(ModelViewSet):
    queryset = Answer.objects.select_related('user').all()
    serializer_class = serializers.AnswerSerializer

    def get_queryset(self):
        return self.queryset.filter(question_id=self.kwargs.get('question_id'))

    def get_permissions(self):
        return [IsAuthenticated(), AnswersPermissions()]
