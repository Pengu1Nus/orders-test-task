"""
Тест API заказов.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from orders.models import Order
from orders.serializers import OrderSerializer

ORDERS_URL = reverse('order:order-list')


def detail_url(order_id):
    """Вспомогательная функция, возвращает url конкретного заказа по id."""
    return reverse('order:order-detail', args=[order_id])


def create_order(user, **params):
    """Вспомогательная функция для создания заказа."""
    defaults = {
        'name': 'Название заказа',
        'description': 'Описание заказа',
    }
    defaults.update(params)

    order = Order.objects.create(user=user, **defaults)
    return order


def create_user(
    email='testmail@example.com', username='testUser', password='testpass1223'
):
    """Вспомогательная функция — создает и возвращает пользователя."""
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password=password,
    )


class PublicOrderApiTests(TestCase):
    """Тест неаутентифицированных запросов."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testnewmail@example.com',
            username='testUser1',
            password='testpass123',
        )
        self.order = Order.objects.create(
            name='Тестовый заказ',
            description='Описание тестового заказа',
            user=self.user,
        )

        self.another_order = create_order(user=self.user, name='Новый заказ')

    def test_filter_orders_by_name(self):
        """Тест фильтрации заказов по названию."""
        response = self.client.get(ORDERS_URL, {'name': 'Тестовый заказ'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.order.name)

    def test_unauthorized_user_cannot_create_order(self):
        """
        Тест случая, когда неавторизованный пользователь
        не может создать заказ.
        """
        payload = {
            'name': 'Название тестового заказа',
            'description': 'Описание заказа',
        }
        res = self.client.post(ORDERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_cannot_delete_order(self):
        """
        Тест случаев, когда неавторизованный пользователь
        не может удалить заказ.
        """
        url = detail_url(self.order.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Order.objects.filter(id=self.order.id).exists())


class PrivateOrdersApiTests(TestCase):
    """Тест заказов для аутентифицированных пользователей."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testnewmail@example.com',
            username='testUser1',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_orders(self):
        """Тест получения списка заказов."""
        create_order(user=self.user)
        create_order(user=self.user)
        create_order(user=self.user)

        res = self.client.get(ORDERS_URL)

        orders = Order.objects.all().order_by('-id')
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_order_detail(self):
        """Тест — получение заказа по id."""
        order = create_order(user=self.user)
        url = detail_url(order.id)
        res = self.client.get(url)

        serializer = OrderSerializer(order)
        self.assertEqual(res.data, serializer.data)

    def test_create_order(self):
        """Тест создания заказа."""
        payload = {
            'name': 'Название заказа',
            'description': 'Описание заказа',
        }
        res = self.client.post(ORDERS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(name=payload['name'])

        self.assertEqual(order.name, payload['name'])
        self.assertEqual(order.description, payload['description'])

    def test_full_update(self):
        """Тест полного обновления заказа."""
        order = create_order(
            user=self.user,
            name='Название заказа',
            description='Описание заказа',
        )

        payload = {
            'name': 'Новое название заказа',
            'description': 'Новое описание заказа',
        }
        url = detail_url(order.id)
        res = self.client.put(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.user, self.user)

    def test_update_user_returns_error(self):
        """
        Тест — попытка изменения автора заказа
        не приводит к изменению автора заказа.
        """
        new_user = create_user(
            email='testsecondmail@example.com',
            username='testUser2',
            password='test123',
        )
        order = create_order(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(order.id)
        self.client.patch(url, payload)

        order.refresh_from_db()
        self.assertEqual(order.user, self.user)

    def test_delete_order(self):
        """Тест удаления заказа."""
        order = create_order(user=self.user)

        url = detail_url(order.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=order.id).exists())

    def test_delete_other_users_order_error(self):
        """Тест — попытка удаления заказа другого автора возвращает ошибку."""
        new_user = create_user(
            email='testdiffmail@example.com',
            username='testAnotherUser2',
            password='test123',
        )
        order = create_order(user=new_user)

        url = detail_url(order.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Order.objects.filter(id=order.id).exists())
