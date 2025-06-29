from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users import models


class UserAdmin(BaseUserAdmin):
    """Определение админки."""

    ordering = ('id',)
    list_display = ('username', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Разрешения'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Временные метки'), {'fields': ('last_login',)}),
    )
    readonly_fields = ('last_login',)
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'age',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
