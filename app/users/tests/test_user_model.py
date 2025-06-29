"""
Тесты модели пользователя.
"""

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    """Класс для теста модели пользователя."""

    def test_create_user_with_username_successful(self):
        """Тест создания пользователя с валидными данными."""
        email = 'testmail@example.com'
        username = 'TestUser'
        password = 'testPass123'
        age = 28

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            age=age,
        )

        self.assertEqual(user.username, username)
        self.assertEqual(user.age, age)
        self.assertTrue(user.check_password(password))

    def test_create_user_without_username_raises_error(self):
        """Тест создания пользователя без юзернейма возвращает ошибку."""
        with self.assertRaises(ValueError):
            User.objects.create_user('', 'testPass123')

    def test_duplicate_email_raises_error(self):
        """
        Тест создания пользователя с существующим email
        возвращает ошибку.
        """
        User.objects.create_user(
            email='testnewmail@example.com',
            username='newUsername',
            password='pass123',
        )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='testnewmail@example.com',
                username='newUsername',
                password='pass456',
            )
