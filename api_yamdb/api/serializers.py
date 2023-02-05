from rest_framework import serializers
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)
from datetime import datetime

from reviews.models import Category, Title, Genre, Comment, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("slug", "name")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("slug", "name")


class TitleDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    description = serializers.CharField(read_only=True, required=False)
    year = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field="slug",
    )
    year = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(int(datetime.now().year))
        ],
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    def create(self, validated_data):
        if Review.objects.filter(
            author=self.context["request"].user,
            title=validated_data.get("title")
        ).exists():
            raise serializers.ValidationError(
                "Нельзя оставить больше одного обзора."
            )
        return Review.objects.create(**validated_data,)

    class Meta:
        model = Review
        exclude = ("title",)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ("review",)
