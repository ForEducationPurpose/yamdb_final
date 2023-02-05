from typing import List

from django.urls import path, include, URLPattern

from .routers import get_users_routes
from .views import sign_up_send_code, authenticate_send_JWT_access

app_name = "users"

v1_users_router: List[URLPattern] = get_users_routes()

urlpatterns = [
    path("auth/signup/", sign_up_send_code, name="signup"),
    path("auth/token/", authenticate_send_JWT_access, name="token"),
    path("", include(v1_users_router)),
]
