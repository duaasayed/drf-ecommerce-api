from rest_framework import serializers
from shop.models import Product
from accounts.models.custom_users import StoreRepresentative
from orders.models import Order, OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(
        slug_field='image', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['brand', 'category', 'title', 'slug',
                  'description', 'price', 'in_stock', 'available', 'rating', 'images']

    def create(self, validated_data):
        validated_data['store'] = self.context['view'].request.user.storerepresentative.store
        return super().create(validated_data)


class RepresentativeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    full_name = serializers.SerializerMethodField()
    added_by = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return str(obj)

    def get_added_by(self, obj):
        return str(obj.added_by) if obj.added_by else None

    class Meta:
        model = StoreRepresentative
        fields = ['full_name', 'first_name', 'last_name',
                  'password', 'password_confirm', 'email', 'added_by']

    def create(self, validated_data):
        user = self.context['view'].request.user.storerepresentative
        validated_data['added_by'] = user
        validated_data['store'] = user.store
        validated_data.pop('password_confirm')
        return StoreRepresentative.objects.create_user(**validated_data)


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'price', 'total_price', 'status']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_products', 'customer',
                  'address', 'payment_method', 'placed_at']
