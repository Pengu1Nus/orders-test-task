from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    ordering = ('-id',)
    readonly_fields = ('created_at',)

    # Запрет на обновление автора заказа через админку.
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields
