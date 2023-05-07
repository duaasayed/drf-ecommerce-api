from rest_framework.viewsets import ModelViewSet
from .models import AddressBook, List, ListProduct
from .serializers import AddressBookSerializer, ListsSerializer, ListProductSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerified, ProfileOwnerPermissions, ListOwnerPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView


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
