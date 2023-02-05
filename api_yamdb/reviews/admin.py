from django.contrib import admin

from .models import Review, Category, Genre, Title, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug", )
    list_display_links = ("pk", "name", )
    search_fields = ("name", )
    list_filter = ("name", )
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug", )
    list_display_links = ("pk", "name", )
    search_fields = ("name", )
    list_filter = ("name", )
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "category", "description", )
    list_display_links = ("pk", "name", )
    search_fields = ("genre", )
    list_filter = ("name", "year", "category", )
    empty_value_display = "-пусто-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "score")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "review", "author", "text", "pub_date")
    search_fields = ("text", )
    list_filter = ("pub_date", )
    empty_value_display = "-пусто-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
