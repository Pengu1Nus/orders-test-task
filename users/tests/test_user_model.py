from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    """Класс для теста модели пользователя."""

    def test_create_user_with_username_successful(self):
        """Тест создания пользователя с валидными данными."""
        username = 'TestUser'
        password = 'testPass123'

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_user_without_username_raises_error(self):
        """Тест создания пользователя без юзернейма возвращает ошибку."""
        with self.assertRaises(ValueError):
            User.objects.create_user('', 'testPass123')

    def test_duplicate_username_raises_error(self):
        """
        Тест создания пользователя с существующим юзернеймом
        возвращает ошибку.
        """
        User.objects.create_user(username='duplicate', password='pass123')

        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='duplicate', password='pass456')
