from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор заказов."""

    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user_id', 'name', 'description')
        read_only_fields = ('id', 'user_id')

    def create(self, validated_data):
        """Создание заказа."""
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновление и возвращение заказа."""
        name = validated_data.pop('name', None)
        description = validated_data.pop('description', None)

        instance = super().update(instance, validated_data)

        if name is not None:
            instance.name = name
        if description is not None:
            instance.description = description

        instance.save()
        return instance
