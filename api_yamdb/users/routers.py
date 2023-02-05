from typing import List

from django.urls import URLPattern
from rest_framework.routers import SimpleRouter

from .views import (UsersViewSet)


def get_users_routes() -> List[URLPattern]:
    """Возвращает список `URLPattern` для эндпоинтов
    users, users/<username>.
    """
    users_router = SimpleRouter()
    users_router.register(r"users", UsersViewSet)
    return users_router.urls
