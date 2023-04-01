from rest_framework.permissions import BasePermission


class AddressBookPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer

    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user.customer
