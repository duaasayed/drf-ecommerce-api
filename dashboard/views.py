from rest_framework.viewsets import ModelViewSet
from accounts.models.custom_users import StoreRepresentative
from shop.models import Product, ProductColor, ProductSize, ProductVariant, ProductSpecification
from orders.models import Order, OrderProduct
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, RepresentativeSerializer, ProductSpecsSerializer, ProductSizesSerializer, ProductVariantSerializer, OrderSerializer, ProductColorSerializer
from .permissions import ProductsPermissions, RepresentativesPermissions, OrdersPermissions


class ProductViewset(ModelViewSet):
    queryset = Product.objects.select_related('store', 'brand', 'category') \
        .prefetch_related('colors__images', 'sizes', 'variants', 'reviews').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ProductsPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(store=store)


class ProductSpecsViewset(ModelViewSet):
    queryset = ProductSpecification.objects.select_related('product').all()
    serializer_class = ProductSpecsSerializer
    permission_classes = [IsAuthenticated, ProductsPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(product__store=store)


class ProductColorsViewset(ModelViewSet):
    queryset = ProductColor.objects.select_related(
        'product').prefetch_related('image').all()
    serializer_class = ProductColorSerializer
    permission_classes = [IsAuthenticated, ProductsPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(product__store=store)


class ProductSizesViewset(ModelViewSet):
    queryset = ProductSize.objects.select_related('product').all()
    serializer_class = ProductSizesSerializer
    permission_classes = [IsAuthenticated, ProductsPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(product__store=store)


class ProductVariantsViewset(ModelViewSet):
    queryset = ProductVariant.objects.select_related(
        'product', 'color', 'size').all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, ProductsPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(product__store=store)


class RepresentativeViewset(ModelViewSet):
    queryset = StoreRepresentative.objects.select_related('added_by').all()
    serializer_class = RepresentativeSerializer
    permission_classes = [IsAuthenticated, RepresentativesPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(store=store)


class OrderViewset(ModelViewSet):
    queryset = OrderProduct.objects.select_related(
        'order__address', 'product').prefetch_related('product__colors__images', 'product__reviews').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrdersPermissions]

    def get_queryset(self):
        store = self.request.user.storerepresentative.store
        return self.queryset.filter(product__store=store)
