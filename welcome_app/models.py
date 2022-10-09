from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from django.contrib.auth.validators import UnicodeUsernameValidator

from uuid import uuid4

from .managers import CustomUserManager


def empty_list() -> list:
    return []

def empty_dict() -> dict:
    return {}

def gen_token() -> str:
    return uuid4()


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        gettext_lazy('username'),
        max_length=50,
        unique=True,
        help_text=gettext_lazy('Обязательное поле. 50 символов и менее: буквы, цифры и @/./+/-/_ '),
        validators=[username_validator],
        error_messages={
            'unique': gettext_lazy("Пользователь с таким именем уже существует."),
        },
    )
    email = models.EmailField(
        gettext_lazy('email address'),
        unique=True,
        help_text=gettext_lazy('Обязательное поле.'),
        error_messages={
            'unique': gettext_lazy("По этой почте уже зарегистрирован аккаунт."),
        },)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_token = models.CharField(default=gen_token, max_length=40, unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'