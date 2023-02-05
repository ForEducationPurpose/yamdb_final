from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Категория произведения"
    )
    slug = models.SlugField(
        unique=True, db_index=True, verbose_name="Слаг категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Жанр произведения")
    slug = models.SlugField(
        unique=True, db_index=True, verbose_name="Слаг жанра"
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256, db_index=True, verbose_name="Название произвведения"
    )
    year = models.IntegerField(
        db_index=True, verbose_name="Год выпуска произведения"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre, through="TitleGenre", related_name="titles", verbose_name="Жанр"
    )
    description = models.TextField(
        blank=True, verbose_name="Описание произведения"
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("-year", "name")

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Произведение"
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name="Жанр"
    )

    def __str__(self):
        return f"{self.title} {self.genre}"


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(
        verbose_name="Текст обзора",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор обзора",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации обзора"
    )
    score = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка произведения",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="one_review_per_title"
            )
        ]

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Обзор на произведение",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    text = models.TextField(verbose_name="Текст комментария")
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации комментария"
    )

    def __str__(self):
        return self.author.username + "_" + self.text[:10]
