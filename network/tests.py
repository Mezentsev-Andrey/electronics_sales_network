from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from network.models import NetworkNode, Product
from users.models import User


class NetworkNodeTestCase(APITestCase):
    """ Тесты модели NetworkNode."""

    def setUp(self):
        """Заполняем БД перед началом тестов."""

        self.userdata = {
            "email": "test@test.ru",
            "password": "12345",
        }
        # создаём пользователя
        user = User.objects.create(email=self.userdata.get("email"), is_active=True)
        user.set_password(self.userdata.get("password"))
        user.save()
        # получаем токен
        response = self.client.post(reverse("users:login"), self.userdata)
        # добавляем токен к авторизации
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.json().get("access")
        )
        # шаблон для создания нового поставщика
        self.factory_data = {
            "title": "Big",
            "email": "big@big.ru",
            "country": "Russia",
            "city": "Moscow",
            "street": "Tverskaya",
            "house": 10,
            "type": "factory",
        }
        self.reseller_data = {
            "title": "Mega",
            "email": "mega@mega.ru",
            "country": "Russia",
            "city": "Moscow",
            "street": "Tverskaya",
            "house": 5,
            "type": "seller",
        }

    def test_node_create(self):
        """ Тест создания звена сети."""

        # Отправка POST-запроса на создание звена сети
        response = self.client.post(
            reverse("network:network_create"), data=self.factory_data
        )
        # Проверка, что статус-код ответа соответствует 201 (Создано)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wrong_factory_with_node_create(self):
        """ Тест валидатора создания звена сети с присвоением задолженности заводу."""

        # Создаем копию данных, чтобы избежать мутации исходных данных
        data = self.factory_data.copy()
        data["debt"] = 50

        # Отправка POST-запроса на создание звена сети с данными, включающими задолженность
        response = self.client.post(reverse("network:network_create"), data=data)
        # Проверка, что статус-код ответа соответствует 400 (Некорректный запрос)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ответ содержит ожидаемое сообщение об ошибке
        self.assertEqual(
            {"non_field_errors": ["Завод не может быть должником по закупкам."]},
            response.json(),
        )

    def test_wrong_factory_with_debt_create(self):
        """ Тест валидатора создания узла сети с присвоением заводу поставщика."""

        # Создание объекта NetworkNode с начальными данными
        self.factory = NetworkNode.objects.create(**self.factory_data)

        # Создаем копию данных, чтобы избежать мутации исходных данных
        data = (
            self.factory_data.copy()
        )  # Создаем копию данных, чтобы избежать мутации исходных данных
        data["title"] = "Big1"
        data["supplier"] = self.factory.id

        # Отправка POST-запроса на создание узла сети с новыми данными
        response = self.client.post(reverse("network:network_create"), data=data)
        # Проверка, что статус-код ответа соответствует 400 (Некорректный запрос)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ответ содержит ожидаемое сообщение об ошибке
        self.assertEqual(
            {"non_field_errors": ["Завод не может закупать товары для реализации."]},
            response.json(),
        )

    def test_wrong_debt_update(self):
        """ Тест валидации запрета обновления через API
        поля «Задолженность перед поставщиком»."""

        # Создание объекта NetworkNode с начальными данными для реселлера
        self.reseller = NetworkNode.objects.create(**self.reseller_data)
        # Отправка PATCH-запроса для обновления debt
        response = self.client.patch(
            reverse("network:network_update", kwargs={"pk": self.reseller.id}),
            {"debt": 5000},
        )
        # Проверка, что ответ содержит ожидаемое сообщение об ошибке
        self.assertEqual(
            {
                "non_field_errors": [
                    "Задолженность перед поставщиком не может быть изменена через API."
                ]
            },
            response.json(),
        )

    def test_node_delete(self):
        """ Тест удаления звена сети."""

        # Создание объекта NetworkNode с начальными данными
        self.factory = NetworkNode.objects.create(**self.factory_data)
        # Отправка DELETE-запроса для удаления узла сети
        response = self.client.delete(
            reverse("network:network_delete", kwargs={"pk": self.factory.pk}),
        )
        # Проверка, что статус-код ответа соответствует 204 (Нет содержимого)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_node_detail(self):
        """ Тест получения одного объекта модели звена сети."""

        # Создание объекта NetworkNode с начальными данными
        self.factory = NetworkNode.objects.create(**self.factory_data)
        # Отправка GET-запроса для получения одного объекта модели
        response = self.client.get(
            reverse("network:network_retrieve", kwargs={"pk": self.factory.pk}),
        )
        # Проверка, что статус-код ответа соответствует 200 (ОК)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_node_list(self):
        """ Тест получения всех объектов модели звена сети."""

        # Создание объекта NetworkNode с начальными данными
        self.factory = NetworkNode.objects.create(**self.factory_data)
        response = self.client.get(
            reverse("network:network_list"),
        )
        # Проверка, что статус-код ответа соответствует 200 (ОК)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductTestCase(APITestCase):
    """ Тесты модели Product."""

    def setUp(self):
        """ Заполняем БД перед началом тестов."""

        self.userdata = {
            "email": "test@test.ru",
            "password": "12345",
        }
        # создаём пользователя
        user = User.objects.create(email=self.userdata.get("email"), is_active=True)
        user.set_password(self.userdata.get("password"))
        user.save()
        # получаем токен
        response = self.client.post(reverse("users:login"), self.userdata)
        # добавляем токен к авторизации
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.json().get("access")
        )
        self.product = Product.objects.create(
            title="New product", model="New model of product"
        )

    def test_create_product(self):
        """ Тест на создание нового продукта."""

        # Проверяем, что отправляем все необходимые поля для создания
        data = {"title": "New product", "model": "New model of product"}

        response = self.client.post("/product/", data, format="json")

        # Проверяем, что статус-код ответа равен 201 Created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что общее количество продуктов в базе данных равно 2.
        self.assertEqual(Product.objects.all().count(), 2)

    def test_list_product(self):
        """ Тест на получение списка продуктов."""

        # Отправляем GET-запрос на URL, соответствующий получению списка продуктов.
        # self.client используется для выполнения запроса в контексте теста.
        response = self.client.get("/product/")

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что общее количество продуктов в базе данных равно 1.
        self.assertEqual(Product.objects.all().count(), 1)

    def retrieve_product(self):
        """ Тест на получение определенного продукта."""

        # Отправляем GET-запрос на URL, соответствующий получению
        # конкретного продукта с идентификатором self.product.id.
        response = self.client.get(f"/product/{self.product.id}/")

        # Проверяем, что статус-код ответа равен 200 OK,
        # что означает успешное получение ресурса.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что значение поля title в данных ответа совпадает
        # со значением поля title у модуля self.product.
        self.assertEqual(response.data["title"], self.product.title)

    def test_update_product(self):
        """ Тест на обновление продукта."""

        # Проверяем, что отправляем все необходимые поля для обновления
        new_data = {"model": "New model of product"}

        # Отправляем PATCH-запрос на URL, соответствующий обновлению продукта с определенным
        # идентификатором self.product.id, с данными для обновления в формате JSON.
        response = self.client.patch(
            f"/product/{self.product.id}/", data=new_data, format="json"
        )

        # Преобразуем тело ответа из формата JSON в Python-словарь.
        data = response.json()

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что значение ключа "model" в JSON-ответе совпадает с обновленным описанием.
        self.assertEqual(data.get("model"), "New model of product")

    def test_delete_product(self):
        """ Тест удаления продукта."""

        # Отправляем DELETE-запрос на URL, соответствующий удалению модуля
        # с определенным идентификатором self.product.id.
        response = self.client.delete(f"/product/{self.product.id}/")

        # Проверяем, что статус-код ответа равен 204 No Content.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверяем, что общее количество продуктов в базе данных равно 0.
        self.assertEqual(Product.objects.all().count(), 0)
