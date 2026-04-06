class OrderData:
    # Тестовые данные для создания заказа
    ORDER_WITH_BLACK_COLOR = {
        "firstName": "Иван",
        "lastName": "Петров",
        "address": "ул. Ленина, 10",
        "metroStation": 1,
        "phone": "+79991234567",
        "rentTime": 5,
        "deliveryDate": "2026-04-10",
        "comment": "Позвонить за час",
        "color": ["BLACK"]
    }
    
    ORDER_WITH_GREY_COLOR = {
        "firstName": "Мария",
        "lastName": "Иванова",
        "address": "пр. Мира, 25",
        "metroStation": 2,
        "phone": "+79876543210",
        "rentTime": 3,
        "deliveryDate": "2026-04-15",
        "comment": "Домофон 123",
        "color": ["GREY"]
    }
    
    ORDER_WITH_BOTH_COLORS = {
        "firstName": "Алексей",
        "lastName": "Сидоров",
        "address": "ул. Пушкина, 5",
        "metroStation": 3,
        "phone": "+79111234567",
        "rentTime": 4,
        "deliveryDate": "2026-04-20",
        "comment": "Оставить у двери",
        "color": ["BLACK", "GREY"]
    }
    
    ORDER_WITHOUT_COLOR = {
        "firstName": "Елена",
        "lastName": "Смирнова",
        "address": "б-р. Строителей, 15",
        "metroStation": 4,
        "phone": "+79221234567",
        "rentTime": 2,
        "deliveryDate": "2026-04-25",
        "comment": "Без самоката не уезжать",
        "color": []
    }
