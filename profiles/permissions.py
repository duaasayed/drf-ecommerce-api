from rest_framework.permissions import BasePermission
from otp_twilio.models import TwilioSMSDevice


class IsVerified(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_customer and user.customer.two_fa_enabled:
            device = TwilioSMSDevice.objects.get(user=user)
            return device.token == None and device.throttling_failure_count == 0
        return True


class ProfileOwnerPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer

    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user.customer


class ListOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.custom_list.customer == request.user.customer
