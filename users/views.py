from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import AuthTokenSerializer, UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """Вью для создания пользователя."""

    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Вью для обновления данных пользователя."""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Получить и вернуть аутентифицированного пользователя."""
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    """Вью для обработки запросов токена."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
