from django.conf import settings
from django.db import models


class Order(models.Model):
    """Модель заказа."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    name = models.CharField(
        'Название',
        max_length=150,
        blank=False,
    )
    description = models.TextField(
        'Описание',
        blank=True,
        help_text='Укажите подробности о заказе, если необходимо.',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.name} (№{self.id})'
