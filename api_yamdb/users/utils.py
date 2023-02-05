import enum


@enum.unique
class Role(str, enum.Enum):
    """Вспомогательный класс для хранения ролей юзеров.
    В питоне3.11 есть StrEnum, здесь эмуляция такого же поведения,
    для представления атрибута как str.
    P.S. Как я хотел сработал не совсем.....но наследование от str я оставил.
    """
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    @staticmethod
    def create_tuple_all_roles():
        """Собирает все объекты имя-значения попарно в один кортеж.
        Данный кортеж подставляется в choices=.
        """
        return tuple((role.value, role.name) for role in Role)

    @staticmethod
    def max_str_length():
        """Динамически связывает величину максимальной строки с max_length
        поля CharField модели, при добавления роли, длина которая будет больше
        максимально существущей, в обязательном порядке
        необходимо провести миграции до добавления новых инстансов.
        """
        return max(len(role.value) for role in Role)
