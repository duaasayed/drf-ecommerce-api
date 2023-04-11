from rest_framework import serializers
from .models import Category, Product, Seller, Brand, Review, Question, Answer


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'show_in_nav']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'show_in_nav', 'subcategories']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo']


class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()
    brand = BrandSerializer()
    category = SubCategorySerializer()
    images = serializers.SlugRelatedField(
        slug_field='url', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['title', 'slug', 'description', 'price', 'rating',
                  'available', 'in_stock', 'seller', 'brand', 'category', 'images']


class BrandDetailsSerializer(serializers.ModelSerializer):
    categories = SubCategorySerializer(many=True)
    sellers = SellerSerializer(many=True)

    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo', 'categories', 'sellers']


class SellerDetailsSerializer(serializers.ModelSerializer):
    categories = SubCategorySerializer(many=True)
    brands = BrandSerializer(many=True)

    class Meta:
        model = Seller
        fields = ['name', 'slug', 'categories', 'brands']


class CategoryDetailsSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True)
    brands = BrandSerializer(many=True)
    sellers = SellerSerializer(many=True)
    best_sellers = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'subcategories',
                  'brands', 'sellers', 'best_sellers']


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
