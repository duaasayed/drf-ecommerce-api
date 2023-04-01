from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import OrdersPermissions


class OrderViewset(ModelViewSet):
    queryset = Order.objects.prefetch_related(
        'order_products__product__images').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrdersPermissions]

    def get_queryset(self):
        auth_user = self.request.user.customer
        return self.queryset.filter(customer=auth_user)
