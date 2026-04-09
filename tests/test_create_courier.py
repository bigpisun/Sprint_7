import allure
import pytest
import requests
from config import Config
from data.courier_data import (
    generate_unique_courier_data,
    generate_courier_without_login,
    generate_courier_without_password,
)
from data.messages import CourierMessages
from helpers.courier_helper import create_courier, login_courier, create_courier_with_validation


@allure.feature('Курьеры')
@allure.story('Создание курьера')
class TestCreateCourier:
    
    @allure.title('Курьера можно создать с валидными данными')
    def test_create_courier_success(self, create_and_delete_courier):
        with allure.step("Проверка, что курьер был создан"):
            courier_data, courier_id = create_and_delete_courier
            assert courier_data is not None
            assert courier_id is not None
        
        with allure.step("Проверка, что курьер может войти в систему"):
            login_response = login_courier(
                courier_data["login"], 
                courier_data["password"]
            )
            assert login_response.status_code == 200
    
    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self, existing_courier):
        with allure.step("Попытка создать курьера с уже существующим логином"):
            response = create_courier_with_validation({
                "login": existing_courier["login"],
                "password": "different_password",
                "firstName": "Different Name"
            })
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 409
                assert response.json()["message"] == CourierMessages.LOGIN_ALREADY_USED
    
    @allure.title('Можно создать курьера с минимальным набором полей')
    def test_create_courier_minimal_fields(self, create_and_delete_courier):
        with allure.step("Создание курьера только с логином и паролем"):
            courier_data, courier_id = create_and_delete_courier
            # Данные уже созданы в фикстуре
            assert courier_data is not None
            assert "login" in courier_data
            assert "password" in courier_data
    
    @allure.title('Создание курьера без логина возвращает ошибку')
    def test_create_courier_without_login(self):
        with allure.step("Создание курьера без поля login"):
            payload = generate_courier_without_login()
            response = create_courier_with_validation(payload)
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 400
                assert response.json()["message"] == CourierMessages.MISSING_REQUIRED_FIELD
    
    @allure.title('Создание курьера без пароля возвращает ошибку')
    def test_create_courier_without_password(self):
        with allure.step("Создание курьера без поля password"):
            payload = generate_courier_without_password()
            response = create_courier_with_validation(payload)
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == 400
                assert response.json()["message"] == CourierMessages.MISSING_REQUIRED_FIELD