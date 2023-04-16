from rest_framework.permissions import BasePermission
from shop.models import Product


class ReviewsPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            user = request.user
            product = view.kwargs.get('product_id')
            has_purchased = user.is_customer and user.customer.has_purchased(
                product)
            return has_purchased
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_customer and user.customer == obj.customer


class QuestionsPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_customer and user.customer == obj.customer


class AnswersPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        product_id = view.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)
        if view.action == 'create' and user.is_customer:
            return user.customer.has_purchased(product_id)
        elif view.action == 'create' and user.is_staff:
            return user.store_representative.store == product.store
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
