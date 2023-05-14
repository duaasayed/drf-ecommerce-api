from rest_framework.viewsets import ModelViewSet
from .models import AddressBook, List, ListProduct
from .serializers import AddressBookSerializer, ListsSerializer, ListProductSerializer, CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerified, ProfileOwnerPermissions, ListOwnerPermission
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from otp_twilio.models import TwilioSMSDevice


class AddressBookViewset(ModelViewSet):
    queryset = AddressBook.objects.all()
    serializer_class = AddressBookSerializer
    permission_classes = [IsAuthenticated, IsVerified, ProfileOwnerPermissions]

    def get_queryset(self):
        auth_user = self.request.user.customer
        return self.queryset.filter(customer=auth_user)

    @action(detail=True, methods=['GET'], url_path='set-default',
            permission_classes=[IsAuthenticated, IsVerified, ProfileOwnerPermissions])
    def set_default(self, request, pk):
        AddressBook.objects.update(is_default=False)
        address = self.get_object()
        address.is_default = True
        address.save()

        serializer = AddressBookSerializer(address)

        return Response(serializer.data)


class ListsViewset(ModelViewSet):
    queryset = List.objects.prefetch_related('products__images').all()
    serializer_class = ListsSerializer
    permission_classes = [IsAuthenticated, IsVerified, ProfileOwnerPermissions]


class ListProductViewset(ModelViewSet):
    queryset = ListProduct.objects.all()
    serializer_class = ListProductSerializer
    permission_classes = [IsAuthenticated, IsVerified, ListOwnerPermission]


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsVerified, ProfileOwnerPermissions])
def manage_2fa(request):
    customer = request.user.customer
    two_fa_enabled = request.data.get('enabled')
    if customer.two_fa_enabled:
        device = TwilioSMSDevice.objects.get(user=customer)
        if device.token or device.throttling_failure_count:
            return Response({'details': 'You do not have permission to perform this action.'})
    customer.two_fa_enabled = two_fa_enabled
    customer.save()
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)
