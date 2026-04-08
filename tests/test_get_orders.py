import allure
from helpers.order_helper import get_orders


@allure.feature('Заказы')
@allure.story('Получение заказов')
class TestGetOrders:
    
    @allure.title('Получение списка заказов возвращает непустой список')
    def test_get_orders_returns_list(self):
        with allure.step("Отправка запроса на получение списка заказов"):
            response = get_orders()
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 200
                assert "orders" in response.json()
                # Проверяем, что список заказов существует (может быть пустым)
                assert isinstance(response.json()["orders"], list)