from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Category, Product, Brand, Seller, Review, Question, Answer
from . import serializers
from .pagination import ProductsPaginator
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductsFilter
from rest_framework.viewsets import ModelViewSet
from .permissions import ReviewsPermissions, QuestionsPermissions, AnswersPermissions
from rest_framework.permissions import IsAuthenticated


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
