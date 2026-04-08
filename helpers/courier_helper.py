import allure
import requests
from config import Config
from data.courier_data import generate_unique_courier_data


def create_courier(payload):
    """Создание курьера с проверкой ответа"""
    with allure.step(f"Отправка запроса на создание курьера с данными: {payload}"):
        response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=payload)
        
        with allure.step("Проверка ответа API"):
            assert response.status_code in [200, 201], \
                f"Ожидался статус 200/201, получен {response.status_code}"
            
            assert "ok" in response.json(), \
                "В ответе отсутствует поле 'ok'"
            
            assert response.json()["ok"] is True, \
                "Значение поля 'ok' должно быть True"
        
        return response


def delete_courier(courier_id):
    """Удаление курьера по ID"""
    with allure.step(f"Отправка запроса на удаление курьера с id={courier_id}"):
        response = requests.delete(f"{Config.BASE_URL}{Config.DELETE_COURIER}/{courier_id}")
        
        with allure.step("Проверка ответа API"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"
            
            assert "ok" in response.json(), \
                "В ответе отсутствует поле 'ok'"
            
            assert response.json()["ok"] is True, \
                "Значение поля 'ok' должно быть True"
        
        return response


def login_courier(login, password):
    """Логин курьера"""
    with allure.step(f"Отправка запроса на логин курьера с логином: {login}"):
        payload = {"login": login, "password": password}
        response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=payload)
        
        with allure.step("Проверка ответа API"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"
            
            assert "id" in response.json(), \
                "В ответе отсутствует поле 'id'"
            
            assert isinstance(response.json()["id"], int), \
                "Поле 'id' должно быть числом"
        
        return response


def create_courier_with_validation(payload):
    """Создание курьера с ожидаемой ошибкой (негативные тесты)"""
    with allure.step(f"Отправка запроса на создание курьера с невалидными данными: {payload}"):
        response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=payload)
        return response


def register_new_courier_and_return_login_password():
    """Регистрация нового курьера и возврат данных для логина"""
    with allure.step("Генерация уникальных данных для нового курьера"):
        courier_data = generate_unique_courier_data()
    
    with allure.step("Отправка запроса на создание курьера"):
        create_response = create_courier(courier_data)
    
    with allure.step("Проверка успешного создания"):
        assert create_response.status_code == 201
    
    return courier_data