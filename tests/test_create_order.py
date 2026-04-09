import allure
import pytest
from data.order_data import DEFAULT_ORDER_DATA, ORDER_WITHOUT_COLOR, ORDER_WITH_BLACK_COLOR, ORDER_WITH_GREY_COLOR, ORDER_WITH_BOTH_COLORS
from helpers.order_helper import create_order


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
    def test_create_order_with_different_colors(self, create_and_cancel_order, order_data):
        with allure.step("Создание заказа"):
            # Фикстура создаст заказ с данными по умолчанию
            # Для разных цветов нужно переопределить
            pass  # TODO: доработать фикстуру для параметризации


@allure.feature('Заказы')
@allure.story('Создание заказа')
class TestCreateOrderSimple:
    
    @allure.title('Можно создать заказ с BLACK цветом')
    def test_create_order_black_color(self, create_and_cancel_order):
        with allure.step("Проверка создания заказа"):
            # Фикстура уже создала заказ с BLACK цветом
            assert create_and_cancel_order is not None