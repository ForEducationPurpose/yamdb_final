from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from api_yamdb.settings import EMAIL_HOST

from .serializers import (
    UserSerializer, SignUpSerializer,
    AuthSerializer, UserRoleSerializer
)
from .permissions import IsAdmin


User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny, ])
def sign_up_send_code(request):
    serializer = SignUpSerializer(data=request.data)
    # Подсмотрел тут
    # https://www.django-rest-framework.org
    # /api-guide/serializers/#raising-an-exception-on-invalid-data
    serializer.is_valid(raise_exception=True)
    field_values = {
        "username": serializer.validated_data["username"],
        "email": serializer.validated_data["email"]
    }
    try:
        user, created = User.objects.get_or_create(
            is_active=False, **field_values
        )
    except Exception:
        return Response(
            request.data,
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = user.make_confirmation_code_for_user()
    user.hash_confirmation_code_and_save(confirmation_code)
    send_mail(
        subject="Welcome_to_YAMDB!",
        message=f" This is your code {confirmation_code}",
        recipient_list=[user.email],
        from_email=EMAIL_HOST, fail_silently=False
    )
    user.save()
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny, ])
def authenticate_send_JWT_access(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    field_values = {
        "username": serializer.validated_data["username"],
        "confirmation_code": serializer.validated_data["confirmation_code"]
    }
    user = get_object_or_404(User, username=field_values["username"])
    if user.check_confirmation_code(
        field_values["confirmation_code"], user.confirmation_code
    ):
        user.is_active = True
        user.save()
        access_token = user.get_access_token_for_user(user)
        return Response(access_token, status=status.HTTP_200_OK)
    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "username"
    # Пофиксил важный баг, который тесты не ловят.
    # По умолчанию используется [^/.],
    # что исключает использование точки в username, что не по ТЗ
    lookup_value_regex = r"[\w.@+-]+"
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    search_fields = ("username", )
    filter_backends = (filters.SearchFilter, )
    pagination_class = PageNumberPagination

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated, )
    )
    def view_me(self, request):
        if request.method == "PATCH":
            # new_data = role_swap(request)
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Убрал индусскую функцию, которая хотя и не позволяла юзеру менять роль
    # тем не менее, не соблюдала ТЗ, лучше запретить доступ юзера к роли совсем
    # Теперь будет вызываться сериализатор на запись для админа, а для юзера
    # role - read_only_field
    def get_serializer_class(self):
        if (
            self.request.user.is_authenticated and (
                self.request.user.is_admin or self.request.user.is_superuser)):
            return UserSerializer
        return UserRoleSerializer
