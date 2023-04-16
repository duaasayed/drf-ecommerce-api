from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProductsPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_store_representative and \
                (request.user.has_perm('shop.add_product')
                 or request.user.storerepresentative.is_admin)
        return request.user.is_store_representative

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update']:
            return request.user.is_store_representative and \
                (request.user.has_perm('shop.change_product')
                 or request.user.storerepresentative.is_admin) and \
                request.user.storerepresentative.store == obj.store
        elif view.action == 'destroy':
            return request.user.is_store_representative and \
                (request.user.has_perm('shop.delete_product')
                 or request.user.storerepresentative.is_admin) and \
                request.user.storerepresentative.store == obj.store
        return request.user.is_store_representative and \
            request.user.storerepresentative.store == obj.store


class RepresentativesPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_store_representative and \
                (request.user.storerepresentative.is_admin or
                 request.user.has_perm('accounts.add_storerepresentative'))
        return request.user.is_store_representative

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update']:
            return request.user.is_store_representative and \
                (request.user.storerepresentative.is_admin or
                 request.user.has_perm('accounts.change_storerepresentative')) and \
                request.user.storerepresentative.store == obj.store
        elif view.action == 'destroy':
            return request.user.is_store_representative and \
                (request.user.storerepresentative.is_admin or
                 request.user.has_perm('accounts.delete_storerepresentative')) and \
                request.user.storerepresentative.store == obj.store
        return request.user.is_store_representative and request.user.storerepresentative.store == obj.store


class OrdersPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return False
        return request.user.is_store_representative

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            return False
        elif view.action in ['update', 'partial_update']:
            return request.user.is_store_representative and request.user.storerepresentative.is_admin
        return request.user.is_store_representative
