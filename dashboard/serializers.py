from rest_framework import serializers
from shop.models import Product
from accounts.models.custom_users import StoreRepresentative
from orders.models import Order, OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(
        slug_field='image', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'brand', 'category', 'title', 'slug',
                  'description', 'price', 'in_stock', 'available', 'rating', 'specs', 'images']

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


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    address = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    placed_at = serializers.SerializerMethodField()
    payment_method = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_address(self, obj):
        return str(obj.order.address)

    def get_phone(self, obj):
        return obj.order.address.phone

    def get_placed_at(self, obj):
        return obj.order.placed_at

    def get_payment_method(self, obj):
        return obj.order.get_payment_method_display()

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'quantity', 'price',
                  'address', 'phone', 'placed_at', 'total_price', 'payment_method', 'status']
