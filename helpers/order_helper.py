import allure
import requests
from config import Config


def create_order(payload):
    """Создание заказа"""
    with allure.step(f"Отправка запроса на создание заказа с данными: {payload}"):
        response = requests.post(f"{Config.BASE_URL}{Config.CREATE_ORDER}", json=payload)
        
        with allure.step("Проверка ответа API"):
            assert response.status_code == 201, \
                f"Ожидался статус 201, получен {response.status_code}"
            
            assert "track" in response.json(), \
                "В ответе отсутствует поле 'track'"
            
            assert isinstance(response.json()["track"], int), \
                "Поле 'track' должно быть числом"
        
        return response


def cancel_order(track_number):
    """Отмена заказа по track номеру"""
    with allure.step(f"Отправка запроса на отмену заказа с track={track_number}"):
        response = requests.put(f"{Config.BASE_URL}{Config.CANCEL_ORDER}", json={"track": track_number})
        
        with allure.step("Проверка ответа API"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"
        
        return response


def get_orders():
    """Получение списка заказов"""
    with allure.step("Отправка запроса на получение списка заказов"):
        response = requests.get(f"{Config.BASE_URL}{Config.GET_ORDERS}")
        
        with allure.step("Проверка ответа API"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"
            
            assert "orders" in response.json(), \
                "В ответе отсутствует поле 'orders'"
        
        return response


def get_order_by_track(track_number):
    """Получение заказа по track номеру"""
    with allure.step(f"Отправка запроса на получение заказа с track={track_number}"):
        response = requests.get(f"{Config.BASE_URL}{Config.GET_ORDER_BY_TRACK}", params={"t": track_number})
        return response


def accept_order(order_id, courier_id):
    """Принятие заказа курьером"""
    with allure.step(f"Отправка запроса на принятие заказа {order_id} курьером {courier_id}"):
        response = requests.put(
            f"{Config.BASE_URL}{Config.ACCEPT_ORDER}/{order_id}", 
            params={"courierId": courier_id}
        )
        return response