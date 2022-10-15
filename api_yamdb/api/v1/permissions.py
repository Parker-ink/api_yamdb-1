from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Доступ предоставляется только администратору.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Полный доступ предоставляется только администратору,
    остальным только читать можно.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """
    Если автор, или модератор, или админ, можно редактировать,
    иначе только читать.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user == obj.author
                or request.user.is_moderator
                or request.user.is_admin
            )
        )
