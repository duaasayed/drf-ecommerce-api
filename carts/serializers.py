from rest_framework import serializers
from .models import Cart, CartProduct
from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'available']


class ReadCartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity', 'total_price']


class WriteCartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']

    def create(self, validated_data):
        cart = self.context['request'].user.customer.cart
        if not cart.has_product(validated_data['product']):
            validated_data['cart'] = cart
            return super().create(validated_data)
        return CartProduct.objects.get(product=validated_data['product'], cart=cart)
