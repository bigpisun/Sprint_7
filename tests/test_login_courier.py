import allure
import pytest
import requests
from config import Config
from data.messages import CourierMessages
from helpers.courier_helper import create_courier, login_courier


@allure.feature('Курьеры')
@allure.story('Логин курьера')
class TestLoginCourier:
    
    @allure.title('Курьер может войти в систему с валидными данными')
    def test_login_courier_success(self, create_and_delete_courier):
        with allure.step("Попытка входа в систему"):
            courier_data = create_and_delete_courier
            response = login_courier(courier_data["login"], courier_data["password"])
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 200
                assert "id" in response.json()
                assert isinstance(response.json()["id"], int)
    
    @allure.title('Логин с неверным паролем возвращает ошибку')
    def test_login_wrong_password(self, existing_courier):
        with allure.step("Попытка входа с неверным паролем"):
            payload = {
                "login": existing_courier["login"],
                "password": "wrong_password"
            }
            response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
            
            with allure.step("Проверка ответа API по документации"):
                assert response.status_code == 404
                assert response.json()["message"] == CourierMessages.LOGIN_NOT_FOUND
    
    @allure.title('Логин с несуществующим логином возвращает ошибку')
    def test_login_nonexistent_login(self):
        with allure.step("Попытка входа с несуществующим логином"):
            payload = {
                "login": "nonexistent_login_12345",
                "password": "any_password"
            }
            response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
            
            with allure.step("Проверка ответа API по документации"):
                assert response.status_code == 404
                assert response.json()["message"] == CourierMessages.LOGIN_NOT_FOUND
    
    @allure.title('Логин без логина возвращает ошибку')
    def test_login_without_login(self):
        with allure.step("Попытка входа без поля login"):
            payload = {"password": "password123"}
            response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
            
            with allure.step("Проверка ответа API по документации"):
                assert response.status_code == 400
                assert response.json()["message"] == CourierMessages.MISSING_REQUIRED_FIELD
    
    @allure.title('Логин без пароля возвращает ошибку')
    def test_login_without_password(self):
        with allure.step("Попытка входа без поля password"):
            payload = {"login": "some_login"}
            response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
            
            with allure.step("Проверка ответа API по документации"):
                assert response.status_code == 400
                assert response.json()["message"] == CourierMessages.MISSING_REQUIRED_FIELD