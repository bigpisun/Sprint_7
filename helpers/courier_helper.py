import requests
import random
import string
from config import Config


def generate_random_string(length=10):
    """Генерация случайной строки"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def register_new_courier_and_return_login_password():
    """Регистрация нового курьера и возврат логина и пароля"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{Config.BASE_URL}{Config.CREATE_COURIER}", json=payload)

    if response.status_code == 201:
        return {"login": login, "password": password, "firstName": first_name, "id": response.json().get("id")}
    return None


def create_test_courier():
    """Создание тестового курьера для удаления после теста"""
    courier = register_new_courier_and_return_login_password()
    
    # Получаем ID курьера после логина
    if courier:
        login_payload = {"login": courier["login"], "password": courier["password"]}
        login_response = requests.post(f"{Config.BASE_URL}{Config.LOGIN_COURIER}", json=login_payload)
        if login_response.status_code == 200:
            courier["id"] = login_response.json().get("id")
    return courier


def delete_courier(courier_id):
    """Удаление курьера по ID"""
    if courier_id:
        response = requests.delete(f"{Config.BASE_URL}{Config.DELETE_COURIER}/{courier_id}")
        return response.status_code == 200
    return False
