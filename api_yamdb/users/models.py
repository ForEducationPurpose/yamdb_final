from typing import Dict

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import LENGTH

from .utils import Role


# Надеюсь, что я понял правильно. Методы убрал в модель.
# Authorization блок вообще удалил, чтобы не плодить прослойки.
# Хотел сделать через manager, чтобы при вызове метода create_user
# автоматически хэш сразу сохранялся в бд, как ты предлагал.
# Не понял как потом из хэша без переопределения кучи методов
# вытащить строку для отправки юзеру. От варианта создания юзера с кодом в БД
# который будет храниться в нехэшированном виде отказался ввиду небезопасности.
class User(AbstractUser):
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )
    role = models.CharField(
        max_length=Role.max_str_length(),
        choices=Role.create_tuple_all_roles(),
        default=Role.USER.value,
        verbose_name="Статус",
    )
    email = models.EmailField(blank=False, unique=True, verbose_name="Почта")
    confirmation_code = models.CharField(max_length=120)

    def __str__(self):
        return self.username

    # По сути принудительная валидация введенных данных админом в поле email db
    def clean(self):
        super().clean()
        EmailValidator(self.email)

    @property
    def is_admin(self) -> bool:
        """Returns `TRUE` if user's `role` is admin."""
        return self.role == Role.ADMIN

    @property
    def is_moderator(self) -> bool:
        """Returns `TRUE` if user's `role` is moderator."""
        return self.role == Role.MODERATOR

    def make_confirmation_code_for_user(self) -> str:
        """Cоздает рандомную строку с помощью функции `get_random_string`,
        по умолчанию длиной 12 символов,  можно изменить через `LENGTH`.
        """
        return get_random_string(length=LENGTH)

    def hash_confirmation_code_and_save(self, confirmation_code) -> None:
        """Хэширует и присваивает атрибуту экземпляра переданную строку
        с помощью функции `make_password` в качестве подписи
        используется `SECRET_KEY`.
        """
        self.confirmation_code = make_password(confirmation_code)

    def check_confirmation_code(
        self, confirmation_code, hashed_confirmation_code
    ) -> bool:
        """ "Сравнивает переданную строку с переданным хэшем
        с помощью джанго функции `check_password`. Возвращает `bool`.
        """
        return check_password(confirmation_code, hashed_confirmation_code)

    def get_access_token_for_user(self) -> Dict[str, str]:
        """Создает access JWT токен с использованием библиотеки `SimpleJWT`."""
        access = AccessToken.for_user(self)
        return {"token": str(access)}

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        #  Если юзернейм будет "me" в базу не запишется
        constraints = (
            models.constraints.CheckConstraint(
                check=~models.Q(username="me"), name="Username_is_not_me"
            ),
        )
