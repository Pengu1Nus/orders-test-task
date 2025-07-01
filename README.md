# 📦 Orders Test Task

Тестовое задание для Backend-разработчика.

## 📚 Описание

Сервис управления заказами, построенный с использованием Django и Django REST Framework (DRF). Предоставляет REST API для взаимодействия с данными заказов.

## ⚙️ Стек технологий

- Python 3.11
- Django 5
- Django REST Framework
- PostgreSQL
- Docker + Docker Compose
- DRF TokenAuthentication (аутентификация по токену)
- DRF Filter (поиск по названию заказов)

## 🚀 Быстрый старт (через Docker)

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Pengu1Nus/orders-test-task.git
   cd orders-test-task
    ```

2. Запустить контейнеры:

    ```bash
    docker compose up --build --abort-on-container-exit
    ```
3. После запуска контейнеров, перейдите в браузере по адресу: http://127.0.0.1:8000/api/docs/

4. Для остановки контейнеров и очистки volumes:

    ```bash
    docker compose down --volumes --remove-orphans
    ```

5. Также, при запущенных контейнах, в дополнительном окне терминала можно создать суперпользователя:

    ```bash
    docker compose exec backend python manage.py createsuperuser
    ```

6. И запустить тесты

    ```bash
    docker compose exec backend python manage.py test
    ```

## 🔐 Эндпоинты пользователей

| Метод | URL                    | Описание                                       | Требуется токен |
|-------|------------------------|------------------------------------------------|-----------------|
| POST  | /api/users/create/     | Создание нового пользователя                   | ❌              |
| POST  | /api/users/token/      | Получение токена (TokenAuthentication)         | ❌              |
| GET   | /api/users/me/         | Получение информации о текущем пользователе    | ✅              |

## 📦 Эндпоинты заказов

| Метод | URL                    | Описание                                       | Требуется токен |
|-------|------------------------|------------------------------------------------|-----------------|
| GET   | /api/orders/           | Получение списка заказов                       | ❌              |
| POST  | /api/orders/           | Создание нового заказа                         | ✅              |
| GET   | /api/orders/{id}/      | Получение информации о заказе по ID            | ❌              |
| PUT   | /api/orders/{id}/      | Полное обновление заказа                       | ✅              |
| PATCH | /api/orders/{id}/      | Частичное обновление заказа                    | ✅              |
| DELETE| /api/orders/{id}/      | Удаление заказа                                | ✅              |
