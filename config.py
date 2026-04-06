class Config:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    # Эндпоинты
    CREATE_COURIER = "/api/v1/courier"
    LOGIN_COURIER = "/api/v1/courier/login"
    CREATE_ORDER = "/api/v1/orders"
    GET_ORDERS = "/api/v1/orders"
    CANCEL_ORDER = "/api/v1/orders/cancel"
    ACCEPT_ORDER = "/api/v1/orders/accept"
    GET_ORDER_BY_TRACK = "/api/v1/orders/track"
    DELETE_COURIER = "/api/v1/courier"
