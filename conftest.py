import pytest
import requests
import allure
from config import Config
from helpers.courier_helper import delete_courier
from helpers.order_helper import cancel_order


@pytest.fixture
def delete_courier_after_test():
    """Фикстура: удаляет курьера после теста (только очистка)"""
    courier_ids = []
    
    yield courier_ids
    
    with allure.step("Очистка: удаление курьеров после теста"):
        for courier_id in courier_ids:
            if courier_id:
                delete_courier(courier_id)


@pytest.fixture
def cancel_order_after_test():
    """Фикстура: отменяет заказ после теста (только очистка)"""
    track_numbers = []
    
    yield track_numbers
    
    with allure.step("Очистка: отмена заказов после теста"):
        for track in track_numbers:
            if track:
                cancel_order(track)