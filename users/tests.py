from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class UserViewSetTests(TestCase):
    def setUp(self):
        """Инициализация клиента API и создание тестового пользователя."""

        # Создание экземпляра клиента API для выполнения запросов к API.
        self.client = APIClient()
        # Данные для создания тестового пользователя.
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }
        # Создание тестового пользователя в базе данных.
        self.user = User.objects.create(**self.user_data)
        # URL для списка пользователей.
        self.list_url = "/users/user/"

    def test_list_users(self):
        """Тестирование получения списка пользователей."""

        # Отправка GET-запроса для получения списка пользователей.
        response = self.client.get(self.list_url)
        # Проверка, что статус-код ответа 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка, что в ответе содержится хотя бы один пользователь.
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_user(self):
        """Тестирование создания нового пользователя."""

        # Данные для нового пользователя.
        new_user_data = {"email": "newuser@example.com", "password": "newpassword123"}
        # Отправка POST-запроса для создания нового пользователя.
        response = self.client.post(self.list_url, new_user_data)
        # Проверка, что статус-код ответа 201 Created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверка, что новый пользователь существует в базе данных.
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_retrieve_user(self):
        """Тестирование получения данных конкретного пользователя."""

        # Отправка GET-запроса для получения данных конкретного пользователя.
        response = self.client.get(f"{self.list_url}{self.user.id}/")
        # Проверка, что статус-код ответа 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка, что email пользователя в ответе соответствует ожидаемому.
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_user(self):
        """Тестирование обновления данных пользователя."""

        # Данные для обновления пользователя.
        updated_data = {"email": "updateduser@example.com"}
        # Отправка PATCH-запроса для обновления данных пользователя.
        response = self.client.patch(f"{self.list_url}{self.user.id}/", updated_data)
        # Проверка, что статус-код ответа 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Обновление данных пользователя из базы данных.
        self.user.refresh_from_db()
        # Проверка, что email пользователя был успешно обновлен.
        self.assertEqual(self.user.email, "updateduser@example.com")

    def test_delete_user(self):
        """Тестирование удаления пользователя."""

        # Отправка DELETE-запроса для удаления пользователя.
        response = self.client.delete(f"{self.list_url}{self.user.id}/")
        # Проверка, что статус-код ответа 204 No Content.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверка, что пользователь был успешно удален из базы данных.
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
