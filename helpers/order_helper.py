import requests
from config import Config


def create_order(order_data):
    """Создание заказа"""
    response = requests.post(f"{Config.BASE_URL}{Config.CREATE_ORDER}", json=order_data)
    return response


def get_order_by_track(track_number):
    """Получение заказа по номеру трека"""
    response = requests.get(f"{Config.BASE_URL}{Config.GET_ORDER_BY_TRACK}", params={"t": track_number})
    return response


def cancel_order(track_number):
    """Отмена заказа по номеру трека"""
    response = requests.put(f"{Config.BASE_URL}{Config.CANCEL_ORDER}", params={"track": track_number})
    return response


def accept_order(order_id, courier_id):
    """Принятие заказа курьером"""
    response = requests.put(f"{Config.BASE_URL}{Config.ACCEPT_ORDER}/{order_id}", params={"courierId": courier_id})
    return response
