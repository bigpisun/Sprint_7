import allure
import pytest
import requests
from config import Config
from data.courier_data import (
    generate_unique_courier_data,
    generate_courier_without_login,
    generate_courier_without_password,
    generate_courier_without_firstname,
    DUPLICATE_COURIER_DATA
)
from data.messages import CourierMessages
from helpers.courier_helper import create_courier, login_courier, create_courier_with_validation


@allure.feature('Курьеры')
@allure.story('Создание курьера')
class TestCreateCourier:
    
    @allure.title('Курьера можно создать с валидными данными')
    def test_create_courier_success(self, create_and_delete_courier):
        with allure.step("Проверка, что курьер был создан"):
            courier_data = create_and_delete_courier
            assert courier_data is not None
            assert "id" in courier_data
        
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
    def test_create_courier_minimal_fields(self):
        with allure.step("Создание курьера только с логином и паролем"):
            courier_data = generate_unique_courier_data()
            minimal_payload = {
                "login": courier_data["login"],
                "password": courier_data["password"]
            }
            
            response = create_courier(minimal_payload)
            
            with allure.step("Очистка: удаление созданного курьера"):
                # Получаем ID курьера
                login_resp = login_courier(courier_data["login"], courier_data["password"])
                if login_resp.status_code == 200:
                    courier_id = login_resp.json()["id"]
                    from helpers.courier_helper import delete_courier
                    delete_courier(courier_id)
    
    @allure.title('Создание курьера без обязательного поля возвращает ошибку')
    @pytest.mark.parametrize("data_generator, expected_status, expected_message", [
        (generate_courier_without_login, 400, CourierMessages.MISSING_REQUIRED_FIELD),
        (generate_courier_without_password, 400, CourierMessages.MISSING_REQUIRED_FIELD),
    ])
    def test_create_courier_missing_fields(self, data_generator, expected_status, expected_message):
        with allure.step("Создание курьера без обязательного поля"):
            payload = data_generator()
            response = create_courier_with_validation(payload)
            
            with allure.step("Проверка ответа API"):
                assert response.status_code == expected_status
                assert response.json()["message"] == expected_message