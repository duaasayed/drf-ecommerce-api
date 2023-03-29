from rest_framework import serializers
from .models import Category, Product, Seller, Brand


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
        fields = ['title', 'slug', 'description', 'price',
                  'available', 'in_stock', 'seller', 'brand', 'category', 'images']
