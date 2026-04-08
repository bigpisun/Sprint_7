import allure
import requests
from config import Config
from data.order_data import DEFAULT_ORDER_DATA, ORDER_WITHOUT_COLOR, ORDER_WITH_BLACK_COLOR, ORDER_WITH_GREY_COLOR, ORDER_WITH_BOTH_COLORS
from helpers.order_helper import create_order


@allure.feature('Заказы')
@allure.story('Создание заказа')
class TestCreateOrder:
    
    @allure.title('Можно создать заказ с разными вариантами цвета')
    @allure.parametrize("order_data", [
        DEFAULT_ORDER_DATA,
        ORDER_WITHOUT_COLOR,
        ORDER_WITH_BLACK_COLOR,
        ORDER_WITH_GREY_COLOR,
        ORDER_WITH_BOTH_COLORS
    ])
    def test_create_order_with_different_colors(self, order_data):
        with allure.step("Создание заказа"):
            response = create_order(order_data)
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 201
                assert "track" in response.json()
                assert isinstance(response.json()["track"], int)
        
        with allure.step("Очистка: отмена заказа"):
            from helpers.order_helper import cancel_order
            cancel_order(response.json()["track"])
    
    @allure.title('Создание заказа без дополнительных полей работает корректно')
    def test_create_order_minimal_fields(self):
        with allure.step("Создание заказа с минимальными данными"):
            minimal_order = {
                "firstName": "Иван",
                "lastName": "Иванов",
                "address": "Москва, ул. Тестовая, 1",
                "metroStation": 4,
                "phone": "+79991234567",
                "rentTime": 5,
                "deliveryDate": "2025-12-31",
                "comment": ""
            }
            response = create_order(minimal_order)
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 201
                assert "track" in response.json()
        
        with allure.step("Очистка: отмена заказа"):
            from helpers.order_helper import cancel_order
            cancel_order(response.json()["track"])