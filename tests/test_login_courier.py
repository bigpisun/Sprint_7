import allure
import pytest
import requests
from config import Config
from helpers.courier_helper import register_new_courier_and_return_login_password, delete_courier


@allure.feature('Логин курьера')
class TestLoginCourier:
    
    @allure.title('Курьер может авторизоваться')
    def test_login_courier_success(self):
        # Создаём курьера
        courier = register_new_courier_and_return_login_password()
        
        # Авторизуемся
        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
        
        assert response.status_code == 200
        assert "id" in response.json()
        
        # Очистка
        courier_id = response.json()["id"]
        delete_courier(courier_id)
    
    @allure.title('Авторизация возвращает id курьера')
    def test_login_returns_id(self):
        courier = register_new_courier_and_return_login_password()
        
        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
        
        assert response.status_code == 200
        assert isinstance(response.json()["id"], int)
        assert response.json()["id"] > 0
        
        # Очистка
        delete_courier(response.json()["id"])
    
    @allure.title('Нельзя авторизоваться без обязательных полей')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_fails(self, missing_field):
        payload = {"login": "test_login", "password": "test_password"}
        del payload[missing_field]
        
        response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"
    
    @allure.title('Ошибка при неверном логине или пароле')
    @pytest.mark.parametrize("login,password", [
        ("wrong_login", "test_password"),
        ("test_login", "wrong_password"),
        ("wrong_login", "wrong_password")
    ])
    def test_login_invalid_credentials_fails(self, login, password):
        # Создаём реального курьера
        courier = register_new_courier_and_return_login_password()
        
        # Пытаемся войти с неверными данными
        payload = {"login": login, "password": password}
        response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
        
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
        
        # Очистка
        if courier and "id" in courier:
            delete_courier(courier["id"])
    
    @allure.title('Ошибка при авторизации несуществующего пользователя')
    def test_login_nonexistent_user_fails(self):
        payload = {
            "login": "nonexistent_user",
            "password": "some_password"
        }
        response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
        
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
