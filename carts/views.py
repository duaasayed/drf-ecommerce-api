from .models import Cart, CartProduct
from .serializers import ReadCartProductSerializer, WriteCartProductSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerified, CartPermissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class CartProductViewset(ModelViewSet):
    queryset = CartProduct.objects.select_related(
        'cart', 'product').prefetch_related('product__colors__images').all()
    permission_classes = [IsAuthenticated, IsVerified, CartPermissions]

    def get_queryset(self):
        auth_user = self.request.user.customer
        cart, _ = Cart.objects.get_or_create(customer=auth_user)
        return self.queryset.filter(cart=cart)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadCartProductSerializer
        return WriteCartProductSerializer

    def list(self, request, *args, **kwargs):
        auth_user = self.request.user.customer
        cart, _ = Cart.objects.prefetch_related(
            'cart_products__product__colors__images').get_or_create(customer=auth_user)
        queryset = cart.cart_products.all()
        serializer = self.get_serializer(queryset, many=True)
        response = {'products': serializer.data,
                    'cart_total_price': cart.total_price}
        return Response(response)
