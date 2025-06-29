"""
Тесты API пользователя.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')


def create_user(**params):
    """Создает и возвращает тестового пользователя."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Тесты API для неаутентифицированных пользователей."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Тест проверки создания юзера с валидными данными."""
        payload = {
            'email': 'testmail@example.com',
            'username': 'testUsername',
            'password': 'testpass123',
            'name': 'Test User',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(username=payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_username_exists_error(self):
        """
        Тест при попытке создания юзера с существующим username,
        пробрасывается ошибка.
        """
        payload = {
            'email': 'differentmail@example.com',
            'username': 'testUsername',
            'password': 'testpass123',
            'age': 30,
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_email_exists_error(self):
        """
        Тест при попытке создания юзера с существующим email,
        пробрасывается ошибка.
        """
        payload = {
            'email': 'testmail@example.com',
            'username': 'testdiffUsername',
            'password': 'testpass123',
            'age': 30,
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """
        Тест, при попытке создания юзера с небезопасным паролем,
        пробрасывается ошибка.
        """
        payload = {
            'email': 'testmail@example.com',
            'username': 'testUsername',
            'password': 'te',
            'age': 30,
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model()
            .objects.filter(username=payload['username'])
            .exists()
        )
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Тест корректного создания токена для валидных данных юзера."""
        user_details = {
            'email': 'testdiffmail@example.com',
            'username': 'testUsername',
            'password': 'testpass123',
            'age': 30,
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'username': user_details['username'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_incorrect_password(self):
        """Тест случая попытки получения токена с некорректным паролем."""
        user_details = {
            'email': 'testmail@example.com',
            'username': 'testUsername',
            'password': 'goodpassword123',
            'age': 30,
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'username': user_details['username'],
            'password': 'differentpassword123',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Тест случая попытки получения токена с пустым паролем."""
        payload = {
            'email': 'testmail@example.com',
            'username': 'testUsername',
            'password': '',
            'age': 30,
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Тест для проверки недоступности эндпоинта
        для неаутентифицированных юзеров.
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
