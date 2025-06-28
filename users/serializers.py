from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта пользователя."""

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'age')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Создает и возвращает пользователя."""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Обновление и возвращение пользователя."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """Валидация данных юзера."""
        username = attrs.get('username')
        password = attrs.get('password')
        age = attrs.get('age')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
            age=age,
        )
        if not user:
            message = _('Не удается войти с введенными данными.')
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs
