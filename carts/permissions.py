from rest_framework import permissions


class CartPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer

    def has_object_permission(self, request, view, obj):
        return obj.cart == request.user.customer.cart
