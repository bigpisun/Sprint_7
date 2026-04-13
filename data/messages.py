class CourierMessages:
    """Класс с ожидаемыми сообщениями для курьеров"""
    LOGIN_ALREADY_USED = "Этот логин уже используется. Попробуйте другой."
    MISSING_REQUIRED_FIELD = "Недостаточно данных для создания учетной записи"
    MISSING_REQUIRED_FIELD_FOR_LOGIN = "Недостаточно данных для входа"
    COURIER_NOT_FOUND = "Курьера с таким id нет."
    LOGIN_NOT_FOUND = "Учетная запись не найдена"
    INCORRECT_PASSWORD = "Неверный пароль"


class OrderMessages:
    """Класс с ожидаемыми сообщениями для заказов"""
    ORDER_NOT_FOUND = "Заказ не найден"
    ORDER_CANCELLED = "Заказ отменен"