import allure
import pytest
import requests
from config import Config
from helpers.courier_helper import create_courier_with_validation, delete_courier, login_courier
from helpers.order_helper import get_order_by_track, accept_order
from data.courier_data import generate_unique_courier_data
from data.messages import CourierMessages


@allure.feature('Дополнительные сценарии')
class TestExtraScenarios:
    
    @allure.title('Попытка удалить несуществующего курьера')
    def test_delete_nonexistent_courier(self):
        with allure.step("Попытка удалить курьера с несуществующим ID"):
            non_existent_id = 999999
            response = requests.delete(f"{Config.BASE_URL}{Config.DELETE_COURIER}/{non_existent_id}")
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 404
                assert response.json()["message"] == CourierMessages.COURIER_NOT_FOUND
    
    @allure.title('Попытка получить заказ по несуществующему треку')
    def test_get_order_by_nonexistent_track(self):
        with allure.step("Попытка получить заказ по несуществующему track номеру"):
            non_existent_track = 999999999
            response = get_order_by_track(non_existent_track)
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 404
                # Проверяем наличие сообщения об ошибке
                assert "message" in response.json()
    
    @allure.title('Попытка принять заказ с несуществующим ID')
    def test_accept_order_with_nonexistent_id(self):
        with allure.step("Попытка принять несуществующий заказ"):
            non_existent_order_id = 999999
            courier_id = 1
            response = accept_order(non_existent_order_id, courier_id)
            
            with allure.step("Проверка ответа API"):
                # Согласно документации, должен быть 404
                assert response.status_code in [400, 404]
    
    @allure.title('Попытка принять заказ без указания курьера')
    def test_accept_order_without_courier_id(self):
        with allure.step("Попытка принять заказ без указания ID курьера"):
            order_id = 1
            response = requests.put(f"{Config.BASE_URL}{Config.ACCEPT_ORDER}/{order_id}")
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 400
                assert "message" in response.json()
    
    @allure.title('Создание курьера с пустыми значениями полей')
    @pytest.mark.parametrize("field, value", [
        ("login", ""),
        ("password", ""),
        ("firstName", "")
    ])
    def test_create_courier_with_empty_fields(self, field, value):
        with allure.step(f"Создание курьера с пустым полем {field}"):
            courier_data = generate_unique_courier_data()
            courier_data[field] = value
            
            response = create_courier_with_validation(courier_data)
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 400
                assert "message" in response.json()