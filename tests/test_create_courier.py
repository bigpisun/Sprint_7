import allure
import requests
from config import Config
from data.courier_data import (
    generate_unique_courier_data,
    generate_courier_without_login,
    generate_courier_without_password,
)
from data.messages import CourierMessages
from helpers.courier_helper import create_courier, login_courier, delete_courier


@allure.feature('Курьеры')
@allure.story('Создание курьера')
class TestCreateCourier:
    
    @allure.title('Курьера можно создать с валидными данными')
    def test_create_courier_success(self, delete_courier_after_test):
        with allure.step("Создание курьера с валидными данными"):
            courier_data = generate_unique_courier_data()
            response = create_courier(courier_data)
            
            assert response.status_code == 201
        
        with allure.step("Получение ID курьера для очистки"):
            login_response = login_courier(courier_data["login"], courier_data["password"])
            courier_id = login_response.json()["id"]
            delete_courier_after_test.append(courier_id)
        
        with allure.step("Проверка, что курьер может войти в систему"):
            login_response = login_courier(courier_data["login"], courier_data["password"])
            assert login_response.status_code == 200
            assert "id" in login_response.json()
    
    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self, delete_courier_after_test):
        with allure.step("Создание первого курьера"):
            courier_data = generate_unique_courier_data()
            response = create_courier(courier_data)
            assert response.status_code == 201
            
            login_response = login_courier(courier_data["login"], courier_data["password"])
            courier_id = login_response.json()["id"]
            delete_courier_after_test.append(courier_id)
        
        with allure.step("Попытка создать курьера с таким же логином"):
            response = requests.post(
                f"{Config.BASE_URL}{Config.CREATE_COURIER}", 
                json=courier_data
            )
            
            assert response.status_code == 409
            assert response.json()["message"] == CourierMessages.LOGIN_ALREADY_USED
    
    @allure.title('Можно создать курьера с минимальным набором полей')
    def test_create_courier_minimal_fields(self, delete_courier_after_test):
        with allure.step("Создание курьера только с логином и паролем"):
            courier_data = generate_unique_courier_data()
            minimal_payload = {
                "login": courier_data["login"],
                "password": courier_data["password"]
            }
            
            response = create_courier(minimal_payload)
            assert response.status_code == 201
            
            login_response = login_courier(courier_data["login"], courier_data["password"])
            courier_id = login_response.json()["id"]
            delete_courier_after_test.append(courier_id)
    
    @allure.title('Создание курьера без логина возвращает ошибку')
    def test_create_courier_without_login(self):
        with allure.step("Создание курьера без поля login"):
            payload = generate_courier_without_login()
            response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=payload)
            
            assert response.status_code == 400
            assert response.json()["message"] == CourierMessages.MISSING_REQUIRED_FIELD
    
    @allure.title('Создание курьера без пароля возвращает ошибку')
    def test_create_courier_without_password(self):
        with allure.step("Создание курьера без поля password"):
            payload = generate_courier_without_password()
            response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=payload)
            
            assert response.status_code == 400
            assert response.json()["message"] == CourierMessages.MISSING_REQUIRED_FIELD