from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "bio", "role", "confirmation_code",
        "username", "first_name", "last_name",
    )
    search_fields = ("username", "role",)
    list_filter = ("username", "role", )
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
