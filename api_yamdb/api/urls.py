from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()

router_v1.register("categories", views.CategoryViewSet, basename="categories")
router_v1.register("genres", views.GenreViewSet, basename="genres")
router_v1.register("titles", views.TitleViewSet, basename="titles")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", views.ReviewViewSet, basename="review"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    views.CommentViewSet,
    basename="comment",
)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/", include("users.urls")),
]
