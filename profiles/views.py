from rest_framework.viewsets import ModelViewSet
from .models import AddressBook
from rest_framework.permissions import IsAuthenticated
from .serializers import AddressBookSerializer
from .permissions import AddressBookPermissions


class AddressBookViewset(ModelViewSet):
    queryset = AddressBook.objects.all()
    serializer_class = AddressBookSerializer
    permission_classes = [IsAuthenticated, AddressBookPermissions]

    def get_queryset(self):
        auth_user = self.request.user.customer
        return self.queryset.filter(customer=auth_user)
