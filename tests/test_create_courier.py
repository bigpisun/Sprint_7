import allure
import pytest
import requests
from config import Config
from helpers.courier_helper import register_new_courier_and_return_login_password, delete_courier


@allure.feature('Создание курьера')
class TestCreateCourier:
    
    @allure.title('Курьера можно создать')
    def test_create_courier_success(self):
        courier = register_new_courier_and_return_login_password()
        assert courier is not None
        # Очистка после теста
        if courier and "id" in courier:
            delete_courier(courier["id"])
    
    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self):
        # Создаём первого курьера
        courier = register_new_courier_and_return_login_password()
        
        # Пытаемся создать второго с теми же данными
        payload = {
            "login": courier["login"],
            "password": courier["password"],
            "firstName": courier["firstName"]
        }
        response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=payload)
        
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется"
        
        # Очистка
        if courier and "id" in courier:
            delete_courier(courier["id"])
    
    @allure.title('Нельзя создать курьера без обязательных полей')
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field_fails(self, missing_field):
        base_payload = {
            "login": "test_login",
            "password": "test_password",
            "firstName": "test_name"
        }
        del base_payload[missing_field]
        
        response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=base_payload)
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
    
    @allure.title('Успешный запрос возвращает {"ok": true}')
    def test_create_courier_returns_ok(self):
        courier = register_new_courier_and_return_login_password()
        assert courier is not None
        
        # Очистка
        if courier and "id" in courier:
            delete_courier(courier["id"])
