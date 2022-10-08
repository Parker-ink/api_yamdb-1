from rest_framework import permissions

from reviews.models import User


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Если автор (отзыва, комментария), то можно разрешить редактировать
    и удалять свои отзывы и комментарии, иначе - только читать
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdmin(permissions.BasePermission):
    """Если роль admin, можно разрешить полный доступ"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == User.ADMIN
                or request.user.is_superuser == User.SUPERUSER
            )
        else:
            return False


class IsModerator(permissions.BasePermission):
    """
    Если роль moderator, можно разрешить редактировать и удалять
    чужие отзывы и комментарии
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == User.MODERATOR
        else:
            return False


class ReadOnly(permissions.BasePermission):
    """Пермишен только для просмотра доступный всем"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
