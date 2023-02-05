import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User

TABLES = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    TitleGenre: "genre_title.csv",
    Review: "review.csv",
    Comment: "comments.csv",
}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for model, file in TABLES.items():
            with open(
                f"{settings.BASE_DIR}/static/data/{file}", "r"
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)
