class  TokensNotAvaleble(Exception):
    """Переменные окружения недоступны."""
    pass


class MessageNotSentInTelegram(Exception):
    """Сообщение в телеграмм бот не отправлено."""
    pass


class ResponseStatusNotOk(Exception):
    """API Яндекс.Домашки временно недоступно."""
    pass


class JSONDecodeErrore(Exception):
    """Ошибка декодинга json в python данные."""
    pass


class ResponseIsNotDict(Exception):
    """Запрос не возвращает словарь данных."""
    pass


class HomeworksNotInResponse(Exception):
    """Ключ homeworks отсутствует в запросе."""
    pass


class CarrentDateNotInResponse(Exception):
    """Ключ current_date отсутствует в запросе."""
    pass


class NoHomeworkData(Exception):
    """Нет данных о домашней работе."""
    pass


class InvalidHomeworkStatus(Exception):
    """Некорректный статус домашней работы."""
    pass
