from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
        Контроллер для создания экземпляров модели Пользователи.
    """

    serializer_class = UserSerializer
    permission_classes = [AllowAny]
