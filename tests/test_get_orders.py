import allure
import requests
from config import Config


@allure.feature('Получение списка заказов')
class TestGetOrders:
    
    @allure.title('Тело ответа возвращает список заказов')
    def test_get_orders_returns_list(self):
        response = requests.get(f"{Config.BASE_URL}{Config.GET_ORDERS}")
        
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
    
    @allure.title('Можно получить заказы с параметрами')
    def test_get_orders_with_params(self):
        params = {
            "limit": 10,
            "page": 0
        }
        response = requests.get(f"{Config.BASE_URL}{Config.GET_ORDERS}", params=params)
        
        assert response.status_code == 200
        assert len(response.json()["orders"]) <= 10
