from rest_framework.permissions import BasePermission


class AddIfNotParent(BasePermission):
    """Разрешенно, если нет родительского комментария"""
    def has_object_permission(self, request, view, obj):
        return bool(not obj.parent)


class IfBasketUser(BasePermission):
    """Разрешенно, если нет родительского комментария"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user.username
