from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Переопределённая модель Пользователя.

        Поля:
            - email: Адрес электронной почты пользователя (уникальный).
            - chat_id: Поле для хранения идентификатора мессенджера Телеграм.
    """
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    chat_id = models.IntegerField(unique=True, max_length=15, verbose_name='идентификатор телеграм')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
