from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешает доступ админу или владельцу бронирования."""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешаеет доступ админу с полными правами или юзеру только чтение."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
            or request.user.is_superuser
        )
