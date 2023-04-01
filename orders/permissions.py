from rest_framework.permissions import BasePermission


class OrdersPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            return obj.customer == request.user.customer and obj.can_be_canceled
        return obj.customer == request.user.customer
