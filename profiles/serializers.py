from rest_framework import serializers
from .models import AddressBook, List, ListProduct
from shop.models import Product
from accounts.models.custom_users import Customer


class AddressBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBook
        fields = '__all__'
        read_only_fields = ['customer']

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user.customer
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(
        slug_field='image', read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'available', 'price',
                  'in_stock', 'brand', 'store', 'category', 'images']


class ListsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ['id', 'name', 'privacy', 'description', 'products']

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user.customer
        return super().create(validated_data)


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListProduct
        fields = ['id', 'custom_list', 'product', 'comment', 'priority']

    def create(self, validated_data):
        list_ = validated_data['custom_list']
        if validated_data['product'] not in list_.products.all():
            return super().create(validated_data)
        return ListProduct.objects.get(product=validated_data['product'])


class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return str(obj)

    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'email',
                  'two_fa_enabled', 'phone', 'email_verified']
