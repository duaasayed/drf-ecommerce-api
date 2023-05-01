from rest_framework.viewsets import ModelViewSet
from accounts.models.custom_users import StoreRepresentative
from shop.models import Product
from orders.models import Order, OrderProduct
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, RepresentativeSerializer, OrderSerializer
from .permissions import ProductsPermissions, RepresentativesPermissions, OrdersPermissions


class ProductViewset(ModelViewSet):
    queryset = Product.objects.select_related('store', 'brand', 'category') \
        .prefetch_related('images', 'reviews').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ProductsPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(store=store)


class RepresentativeViewset(ModelViewSet):
    queryset = StoreRepresentative.objects.select_related('added_by').all()
    serializer_class = RepresentativeSerializer
    permission_classes = [IsAuthenticated, RepresentativesPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(store=store)


class OrderViewset(ModelViewSet):
    queryset = OrderProduct.objects.select_related(
        'order__address', 'product').prefetch_related('product__images', 'product__reviews').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrdersPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(product__store=store)
