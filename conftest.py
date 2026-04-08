import pytest
import requests
import allure
from config import Config
from helpers.courier_helper import create_courier, delete_courier
from helpers.order_helper import cancel_order


@pytest.fixture
def create_and_delete_courier():
    """Фикстура: создаёт курьера и удаляет его после теста"""
    courier_data = None
    created_courier_id = None
    
    with allure.step("Создание курьера для теста"):
        # Генерируем уникальные данные
        import random
        import string
        login = f"test_courier_{random.randint(1000, 9999)}"
        password = "password123"
        first_name = "Test"
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=payload)
        
        if response.status_code == 201:
            # Получаем ID курьера через логин
            login_response = requests.post(
                f"{Config.BASE_URL}{Config.LOGIN_COURIER}", 
                json={"login": login, "password": password}
            )
            if login_response.status_code == 200:
                created_courier_id = login_response.json().get("id")
                courier_data = {
                    "id": created_courier_id,
                    "login": login,
                    "password": password,
                    "first_name": first_name
                }
    
    yield courier_data
    
    with allure.step("Удаление курьера после теста (пост-условие)"):
        if created_courier_id:
            delete_courier(created_courier_id)


@pytest.fixture
def create_and_cancel_order():
    """Фикстура: создаёт заказ и отменяет его после теста"""
    track_number = None
    
    with allure.step("Создание заказа для теста"):
        payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Москва, ул. Тестовая, 1",
            "metroStation": 4,
            "phone": "+79991234567",
            "rentTime": 5,
            "deliveryDate": "2025-12-31",
            "comment": "Тестовый заказ",
            "color": ["BLACK"]
        }
        
        response = requests.post(f"{Config.BASE_URL}{Config.CREATE_ORDER}", json=payload)
        
        if response.status_code == 201 and "track" in response.json():
            track_number = response.json()["track"]
    
    yield track_number
    
    with allure.step("Отмена заказа после теста (пост-условие)"):
        if track_number:
            cancel_order(track_number)


@pytest.fixture
def existing_courier():
    """Фикстура: создаёт и возвращает существующего курьера для тестов"""
    with allure.step("Создание существующего курьера как предусловие"):
        import random
        import string
        login = f"existing_courier_{random.randint(1000, 9999)}"
        password = "password123"
        first_name = "Existing"
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=payload)
        
        courier_id = None
        if response.status_code == 201:
            login_response = requests.post(
                f"{Config.BASE_URL}{Config.LOGIN_COURIER}", 
                json={"login": login, "password": password}
            )
            if login_response.status_code == 200:
                courier_id = login_response.json().get("id")
        
        yield {
            "login": login,
            "password": password,
            "first_name": first_name,
            "id": courier_id
        }
        
        with allure.step("Очистка: удаление курьера"):
            if courier_id:
                delete_courier(courier_id)