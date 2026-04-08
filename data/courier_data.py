import random
import string


def generate_unique_courier_data():
    """Генерирует уникальные данные для курьера"""
    login = f"courier_{random.randint(10000, 99999)}"
    password = f"pass_{random.randint(1000, 9999)}"
    first_name = f"Name_{random.randint(1, 100)}"
    
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }


def generate_courier_without_login():
    """Генерирует данные курьера без поля login"""
    data = generate_unique_courier_data()
    del data["login"]
    return data


def generate_courier_without_password():
    """Генерирует данные курьера без поля password"""
    data = generate_unique_courier_data()
    del data["password"]
    return data


def generate_courier_without_firstname():
    """Генерирует данные курьера без поля firstName"""
    data = generate_unique_courier_data()
    del data["firstName"]
    return data


# Шаблоны для тестов
VALID_COURIER_DATA = {
    "login": "valid_courier",
    "password": "valid_pass",
    "firstName": "Valid"
}

DUPLICATE_COURIER_DATA = {
    "login": "duplicate_courier",
    "password": "pass123",
    "firstName": "Duplicate"
}