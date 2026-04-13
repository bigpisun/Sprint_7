import allure
import pytest
import requests
from config import Config
from data.messages import CourierMessages
from helpers.courier_helper import login_courier, delete_courier


@allure.feature('Курьеры')
@allure.story('Логин курьера')
class TestLoginCourier:
    
    @allure.title('Курьер может войти в систему с валидными данными')
    def test_login_courier_success(self, delete_courier_after_test):
        with allure.step("Создание курьера для теста"):
            from data.courier_data import generate_unique_courier_data
            courier_data = generate_unique_courier_data()
            
            response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=courier_data)
            assert response.status_code == 201
            
            login_resp = login_courier(courier_data["login"], courier_data["password"])
            courier_id = login_resp.json()["id"]
            delete_courier_after_test.append(courier_id)
        
        with allure.step("Попытка входа в систему"):
            response = login_courier(courier_data["login"], courier_data["password"])
            
            assert response.status_code == 200
            assert "id" in response.json()
            assert isinstance(response.json()["id"], int)
    
    @allure.title('Логин с неверным паролем возвращает ошибку')
    def test_login_wrong_password(self, delete_courier_after_test):
        with allure.step("Создание курьера для теста"):
            from data.courier_data import generate_unique_courier_data
            courier_data = generate_unique_courier_data()
            
            response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=courier_data)
            assert response.status_code == 201
            
            login_resp = login_courier(courier_data["login"], courier_data["password"])
            courier_id = login_resp.json()["id"]
            delete_courier_after_test.append(courier_id)
        
        with allure.step("Попытка входа с неверным паролем"):
            payload = {
                "login": courier_data["login"],
                "password": "wrong_password"
            }
            response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
            
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
            
            assert response.status_code == 404
            assert response.json()["message"] == CourierMessages.LOGIN_NOT_FOUND
    
    @allure.title('Логин без логина возвращает ошибку')
    def test_login_without_login(self):
        with allure.step("Попытка входа без поля login"):
            payload = {"password": "password123"}
            response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
            
            assert response.status_code == 400
            assert "message" in response.json()
    
    @allure.title('Логин без пароля возвращает ошибку')
    def test_login_without_password(self):
        with allure.step("Попытка входа без поля password"):
            payload = {"login": "some_login"}
            response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
            
            # По документации API должен возвращаться статус 400
            # Баг сервера: возвращается 504 Service Unavailable
            # Ожидаемый статус по документации: 400
            expected_status = 400
            actual_status = response.status_code
            
            if actual_status == 504:
                pytest.xfail("Баг сервера: при запросе без пароля возвращается 504 вместо 400")
            
            assert actual_status == expected_status, \
                f"Ожидался статус {expected_status}, получен {actual_status}"
            assert "message" in response.json()