from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from reviews.models import Category, Genre, Title, Review
from users.permissions import IsAdminOrModeratorOrAuthor, IsAdminOrReadOnly
from .filters import TitleFilterFields
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    CategorySerializer, GenreSerializer, TitlePostSerializer,
    CommentSerializer, ReviewSerializer, TitleDetailSerializer
)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", )
    ordering_fields = ("name", )
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", )
    ordering_fields = ("name", )
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = "slug"


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilterFields
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleDetailSerializer
        return TitlePostSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrAuthor, )

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)

        return title

    def get_queryset(self):
        title = self.get_title()
        queryset = title.reviews.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrAuthor, )

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = review.comments.all()

        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
