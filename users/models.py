from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(120)],
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
