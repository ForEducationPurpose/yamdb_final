from typing import List

from django.urls import URLPattern, include, path

from .routers import get_users_routes
from .views import authenticate_send_jwt_access, sign_up_send_code

app_name = "users"

v1_users_router: List[URLPattern] = get_users_routes()

urlpatterns = [
    path("auth/signup/", sign_up_send_code, name="signup"),
    path("auth/token/", authenticate_send_jwt_access, name="token"),
    path("", include(v1_users_router)),
]
