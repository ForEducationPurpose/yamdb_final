from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """"Класс содержит разрешения только админу и суперюзеру.
    Юзер должен быть с токеном.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and (user.is_admin or user.is_superuser)
        )


class IsAdminOrReadOnly(BasePermission):
    """Класс содержит разрешения для всех, если метод GET, HEAD, OPTIONS.
    Или полный комплект только если юзер с токеном и при этом
    админ или суперюзер.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            request.method in SAFE_METHODS
            or (user.is_authenticated
                and (user.is_admin or user.is_superuser))
        )


class IsAdminOrModeratorOrAuthor(BasePermission):
    """Класс содержит разрешения для всех, если метод GET, HEAD, OPTIONS
    или юзер с токеном.
    Права доступа к отдельным объектам,
    если методы не GET, HEAD, OPTIONS,
    получают модератор, админ, автор объекта и суперюзер.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    # Отдельные объекты он может удалять и т.п.
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in SAFE_METHODS
            or obj.author == user
            or user.is_moderator
            or user.is_admin
            or user.is_superuser
        )
