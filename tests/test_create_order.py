import allure
import pytest
from helpers.order_helper import create_order, cancel_order
from data.order_data import OrderData


@allure.feature('Создание заказа')
class TestCreateOrder:
    
    @allure.title('Можно указать один цвет - BLACK')
    def test_create_order_with_black_color(self):
        response = create_order(OrderData.ORDER_WITH_BLACK_COLOR)
        assert response.status_code == 201
        assert "track" in response.json()
        # Очистка
        cancel_order(response.json()["track"])
    
    @allure.title('Можно указать один цвет - GREY')
    def test_create_order_with_grey_color(self):
        response = create_order(OrderData.ORDER_WITH_GREY_COLOR)
        assert response.status_code == 201
        assert "track" in response.json()
        # Очистка
        cancel_order(response.json()["track"])
    
    @allure.title('Можно указать оба цвета')
    def test_create_order_with_both_colors(self):
        response = create_order(OrderData.ORDER_WITH_BOTH_COLORS)
        assert response.status_code == 201
        assert "track" in response.json()
        # Очистка
        cancel_order(response.json()["track"])
    
    @allure.title('Можно не указывать цвет')
    def test_create_order_without_color(self):
        response = create_order(OrderData.ORDER_WITHOUT_COLOR)
        assert response.status_code == 201
        assert "track" in response.json()
        # Очистка
        cancel_order(response.json()["track"])
    
    @allure.title('Тело ответа содержит track')
    @pytest.mark.parametrize("order_data", [
        OrderData.ORDER_WITH_BLACK_COLOR,
        OrderData.ORDER_WITH_GREY_COLOR,
        OrderData.ORDER_WITH_BOTH_COLORS,
        OrderData.ORDER_WITHOUT_COLOR
    ])
    def test_order_response_contains_track(self, order_data):
        response = create_order(order_data)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
        # Очистка
        cancel_order(response.json()["track"])
