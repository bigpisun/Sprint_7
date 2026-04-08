class OrderColors:
    BLACK = ["BLACK"]
    GREY = ["GREY"]
    BOTH = ["BLACK", "GREY"]
    NONE = []


def generate_order_data(color=None):
    """Генерирует данные для заказа с указанным цветом"""
    base_order = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "Москва, ул. Тестовая, 1",
        "metroStation": 4,
        "phone": "+79991234567",
        "rentTime": 5,
        "deliveryDate": "2025-12-31",
        "comment": "Тестовый заказ"
    }
    
    if color is not None:
        base_order["color"] = color
    
    return base_order


# Стандартные данные для тестов
DEFAULT_ORDER_DATA = generate_order_data(OrderColors.BLACK)
ORDER_WITHOUT_COLOR = generate_order_data(None)
ORDER_WITH_BLACK_COLOR = generate_order_data(OrderColors.BLACK)
ORDER_WITH_GREY_COLOR = generate_order_data(OrderColors.GREY)
ORDER_WITH_BOTH_COLORS = generate_order_data(OrderColors.BOTH)