from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # Регулярное выражение соответствует используемому в модели,
    # django.contrib.auth.validators.UnicodeUsernameValidator
    # Letters, digits and @/./+/-/_
    username = serializers.RegexField(
        max_length=150, regex=r"^[\w.@+-]+$", required=True
    )
    email = serializers.EmailField(max_length=254, required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate_username(self, username):
        if username.lower() == "me":
            raise serializers.ValidationError(
                "Нельзя использовать me в качестве юзернейма"
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "Этот юзернейм занят, выберите другой"
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Эта почта уже занята")
        return email

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserRoleSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150, regex=r"^[\w.@+-]+$", required=True
    )
    email = serializers.EmailField(max_length=254, required=True)

    def validate_username(self, username):
        return UserSerializer.validate_username(self, username)

    def validate_email(self, email):
        return UserSerializer.validate_email(self, email)


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
