from rest_framework.viewsets import ModelViewSet
from .models import AddressBook
from .serializers import AddressBookSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerified, AddressBookPermissions
from rest_framework.decorators import action
from rest_framework.response import Response


class AddressBookViewset(ModelViewSet):
    queryset = AddressBook.objects.all()
    serializer_class = AddressBookSerializer
    permission_classes = [IsAuthenticated, IsVerified, AddressBookPermissions]

    def get_queryset(self):
        auth_user = self.request.user.customer
        return self.queryset.filter(customer=auth_user)

    @action(detail=True, methods=['GET'], url_path='set-default',
            permission_classes=[IsAuthenticated, IsVerified, AddressBookPermissions])
    def set_default(self, request, pk):
        AddressBook.objects.update(is_default=False)
        address = self.get_object()
        address.is_default = True
        address.save()

        serializer = AddressBookSerializer(address)

        return Response(serializer.data)
