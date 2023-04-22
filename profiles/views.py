from rest_framework.viewsets import ModelViewSet
from .models import AddressBook
from .serializers import AddressBookSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerified, AddressBookPermissions


class AddressBookViewset(ModelViewSet):
    queryset = AddressBook.objects.all()
    serializer_class = AddressBookSerializer
    permission_classes = [IsAuthenticated, IsVerified, AddressBookPermissions]

    def get_queryset(self):
        auth_user = self.request.user.customer
        return self.queryset.filter(customer=auth_user)
