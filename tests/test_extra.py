import allure
import pytest
import requests
from config import Config
from helpers.courier_helper import register_new_courier_and_return_login_password, delete_courier
from helpers.order_helper import create_order, cancel_order, get_order_by_track, accept_order
from data.order_data import OrderData


@allure.feature('Дополнительные тесты')
class TestExtra:
    
    @allure.title('Удаление курьера - успешный запрос')
    def test_delete_courier_success(self):
        courier = register_new_courier_and_return_login_password()
        
        # Получаем ID через логин
        login_payload = {"login": courier["login"], "password": courier["password"]}
        login_response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=login_payload)
        courier_id = login_response.json()["id"]
        
        response = requests.delete(f"{Config.BASE_URL}{Config.DELETE_COURIER}/{courier_id}")
        
        assert response.status_code == 200
        assert response.json()["ok"] == True
    
    @allure.title('Удаление курьера без id - ошибка')
    def test_delete_courier_without_id_fails(self):
        response = requests.delete(f"{Config.BASE_URL}{Config.DELETE_COURIER}/")
        
        assert response.status_code == 404
    
    @allure.title('Удаление курьера с несуществующим id - ошибка')
    def test_delete_courier_invalid_id_fails(self):
        response = requests.delete(f"{Config.BASE_URL}{Config.DELETE_COURIER}/999999")
        
        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id нет"
    
    @allure.title('Принятие заказа - успешный запрос')
    def test_accept_order_success(self):
        # Создаём курьера
        courier = register_new_courier_and_return_login_password()
        login_payload = {"login": courier["login"], "password": courier["password"]}
        login_response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=login_payload)
        courier_id = login_response.json()["id"]
        
        # Создаём заказ
        order_response = create_order(OrderData.ORDER_WITHOUT_COLOR)
        order_id = order_response.json()["track"]
        
        # Принимаем заказ
        response = accept_order(order_id, courier_id)
        
        assert response.status_code == 200
        assert response.json()["ok"] == True
        
        # Очистка
        delete_courier(courier_id)
        cancel_order(order_id)
    
    @allure.title('Принятие заказа без id курьера - ошибка')
    def test_accept_order_without_courier_id_fails(self):
        order_response = create_order(OrderData.ORDER_WITHOUT_COLOR)
        order_id = order_response.json()["track"]
        
        response = accept_order(order_id, None)
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"
        
        # Очистка
        cancel_order(order_id)
    
    @allure.title('Получение заказа по номеру - успешный запрос')
    def test_get_order_by_track_success(self):
        order_response = create_order(OrderData.ORDER_WITHOUT_COLOR)
        track_number = order_response.json()["track"]
        
        response = get_order_by_track(track_number)
        
        assert response.status_code == 200
        assert "order" in response.json()
        
        # Очистка
        cancel_order(track_number)
    
    @allure.title('Получение заказа без номера - ошибка')
    def test_get_order_without_track_fails(self):
        response = get_order_by_track(None)
        
        assert response.status_code == 400
    
    @allure.title('Получение заказа с несуществующим номером - ошибка')
    def test_get_order_invalid_track_fails(self):
        response = get_order_by_track(999999999)
        
        assert response.status_code == 404
        assert response.json()["message"] == "Заказ не найден"
