from rest_framework import serializers
from .models import Category, Product, Store, Brand, Review, Question, Answer


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'show_in_nav']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'show_in_nav', 'subcategories']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo']


class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    brand = BrandSerializer()
    category = SubCategorySerializer()
    images = serializers.SlugRelatedField(
        slug_field='url', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['title', 'slug', 'description', 'price', 'rating',
                  'available', 'in_stock', 'store', 'brand', 'category', 'images']


class BrandDetailsSerializer(serializers.ModelSerializer):
    categories = SubCategorySerializer(many=True)
    stores = StoreSerializer(many=True)

    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo', 'categories', 'stores']


class StoreDetailsSerializer(serializers.ModelSerializer):
    categories = SubCategorySerializer(many=True)
    brands = BrandSerializer(many=True)

    class Meta:
        model = Store
        fields = ['name', 'slug', 'categories', 'brands']


class CategoryDetailsSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True)
    brands = BrandSerializer(many=True)
    stores = StoreSerializer(many=True)
    best_sellers = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'subcategories',
                  'brands', 'stores', 'best_sellers']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='customer', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'author', 'content', 'stars']

    def create(self, validated_data):
        validated_data['product_id'] = self.context['view'].kwargs.get(
            'product_id')
        validated_data['customer'] = self.context['request'].user.customer
        return super().create(validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'author', 'content', 'verified']

    def create(self, validated_data):
        validated_data['question_id'] = self.context['view'].kwargs.get(
            'question_id')
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='customer', read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'author', 'content', 'answers']

    def create(self, validated_data):
        validated_data['product_id'] = self.context['view'].kwargs.get(
            'product_id')
        validated_data['customer'] = self.context['request'].user.customer
        return super().create(validated_data)


class RelatedRroductSerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(
        slug_field='image', read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'images', 'rating']
