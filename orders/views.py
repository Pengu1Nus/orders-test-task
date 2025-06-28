"""
Вью для API заказов.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from orders import filters, serializers

from .models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """Вью для API заказов."""

    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all().order_by('-id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    filterset_class = filters.OrderFilter

    def destroy(self, request, *args, **kwargs):
        """Удаление заказа доступно только его автору."""

        instance = self.get_object()

        if instance.user != request.user:
            return Response(
                {'detail': 'Вы можете удалить только свои заказы.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        """Возвращает сериализатор класса, в зависимости от типа action."""
        if self.action == 'list':
            return serializers.OrderSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Создание нового заказа."""
        serializer.save(user=self.request.user)
