from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField('Email', unique=True, blank=True)
    password = models.CharField('Пароль', max_length=128)
    age = models.PositiveSmallIntegerField(
        'Возраст',
        null=True,
        blank=True,
        validators=[MaxValueValidator(120)],
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
