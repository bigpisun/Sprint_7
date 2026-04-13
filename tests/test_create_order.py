import allure
import pytest
import requests
from config import Config
from data.order_data import (
    DEFAULT_ORDER_DATA, 
    ORDER_WITHOUT_COLOR, 
    ORDER_WITH_BLACK_COLOR, 
    ORDER_WITH_GREY_COLOR, 
    ORDER_WITH_BOTH_COLORS
)
from helpers.order_helper import cancel_order


@allure.feature('Заказы')
@allure.story('Создание заказа')
class TestCreateOrder:
    
    @allure.title('Можно создать заказ с разными вариантами цвета')
    @pytest.mark.parametrize("order_data", [
        DEFAULT_ORDER_DATA,
        ORDER_WITHOUT_COLOR,
        ORDER_WITH_BLACK_COLOR,
        ORDER_WITH_GREY_COLOR,
        ORDER_WITH_BOTH_COLORS
    ])
    def test_create_order_with_different_colors(self, cancel_order_after_test, order_data):
        with allure.step("Создание заказа"):
            response = requests.post(f"{Config.BASE_URL}{Config.CREATE_ORDER}", json=order_data)
            
            assert response.status_code == 201
            assert "track" in response.json()
            assert isinstance(response.json()["track"], int)
            
            track = response.json()["track"]
            cancel_order_after_test.append(track)
    
    @allure.title('Можно создать заказ с BLACK цветом')
    def test_create_order_black_color(self, cancel_order_after_test):
        with allure.step("Создание заказа с цветом BLACK"):
            order_data = ORDER_WITH_BLACK_COLOR
            response = requests.post(f"{Config.BASE_URL}{Config.CREATE_ORDER}", json=order_data)
            
            assert response.status_code == 201
            assert "track" in response.json()
            
            track = response.json()["track"]
            cancel_order_after_test.append(track)
    
    @allure.title('Создание заказа без дополнительных полей работает корректно')
    def test_create_order_minimal_fields(self, cancel_order_after_test):
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
            response = requests.post(f"{Config.BASE_URL}{Config.CREATE_ORDER}", json=minimal_order)
            
            assert response.status_code == 201
            assert "track" in response.json()
            
            track = response.json()["track"]
            cancel_order_after_test.append(track)