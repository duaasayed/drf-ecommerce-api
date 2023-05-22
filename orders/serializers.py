from rest_framework import serializers
from .models import Order, OrderProduct, OrderChangeHistory
from carts.models import Cart
from shop.models import Product
from django.utils.translation import gettext as _


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Order
        fields = ['id', 'order_products', 'payment_method',
                  'placed_at', 'total_price', 'address', 'status']
        read_only_fields = ['id', 'placed_at', 'total_price']

    def create(self, validated_data):
        customer = self.context['request'].user.customer
        cart = Cart.objects.prefetch_related(
            'cart_products').get(customer=customer)
        order = Order.objects.create(customer=customer, **validated_data)
        for cart_product in cart.cart_products.select_related('product').all():
            if cart_product.product.available:
                # if cart_product.product.in_stock >= cart_product.quantity and cart_product.product.available:
                order.order_products.create(
                    product=cart_product.product, price=cart_product.price, quantity=cart_product.quantity)
        cart.clear()
        return order


class OrderTracking(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return _(obj.get_status_display())

    class Meta:
        model = OrderChangeHistory
        fields = ['order_id', 'location', 'status', 'created_at']
