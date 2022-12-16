import logging
import os
import time
from sys import exit, stdout

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

HTTP_STATUS_OK = 200
LAST_HOMEWORK_INDEX = 0


def check_tokens() -> bool:
    """Проверяем доступность переменных окружения."""
    return all([TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, PRACTICUM_TOKEN])


def send_message(bot: telegram.bot.Bot, message: str) -> None:
    """Отправляем сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(f'Бот успешно отправил сообщение: {message}')
    except Exception as errore:
        message = f'Бот не отправил сообщение по причине: {errore}'
        logging.error(message)
        raise exceptions.MessageNotSentInTelegram(message)
    else:
        logging.debug(f'Бот успешно отправил сообщение: {message}')


def get_api_answer(timestamp: int) -> dict:
    """Делаем запрос к эндпоинту API-сервиса."""
    PAYLOAD = {'from_date': timestamp}
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=PAYLOAD
        )
        if response.status_code != HTTP_STATUS_OK:
            message = (
                'API недоступен. '
                f'Статус ответа - {response.status_code}, '
                f'по причине - {response.reason}, '
                f'текст ответа - {response.text}.'
            )
            logging.error(message)
            raise exceptions.ResponseStatusNotOk(message)
    except requests.RequestException:
        logging.error(message)
        raise requests.RequestException(message)
    else:
        return response.json()


def check_response(response: dict) -> list:
    """Проверяем ответ API на соответствие документации."""
    try:
        isinstance(response, dict)
    except TypeError:
        message = 'Неверный тип полученных данных.'
        logging.error(message)
        raise exceptions.ResponseIsNotDict(message)
    try:
        homeworks = response['homeworks']
        if not isinstance(homeworks, list):
            message = 'Список домашних работ не является списком.'
            logging.error(message)
            raise TypeError(message)
    except KeyError:
        message = 'Ключ homeworks отсутствует в словаре.'
        logging.error(message)
        raise exceptions.HomeworksNotInResponse(message)
    try:
        current_date = response['current_date']
        if not isinstance(current_date, int):
            message = 'Current_date не является целым числом.'
            logging.error(message)
            raise TypeError(message)
    except KeyError:
        message = 'Ключ current_date отсутствует в словаре.'
        logging.error(message)
        raise exceptions.CarrentDateNotInResponse(message)
    else:
        return homeworks


def parse_status(homework: dict) -> str:
    """
    Извлекаем из информации о конкретной домашней работе статус этой работы.
    """
    try:
        homework_name = homework['homework_name']
        status = homework['status']
    except KeyError:
        message = 'Отсутствуют данные о домашней работе.'
        logging.error(message)
        raise exceptions.NoHomeworkData(message)
    try:
        verdict = HOMEWORK_VERDICTS[status]
    except KeyError:
        message = 'Статус домашней работы не соответствует ожидаемому.'
        logging.error(message)
        raise exceptions.InvalidHomeworkStatus(message)
    else:
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        message = 'Бот остановлен, отсутствует временная переменная.'
        logging.critical(message)
        raise exit(message)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time()) - RETRY_PERIOD
    message = ''
    last_message = ''
    latest_error = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            message = (
                parse_status(homeworks[LAST_HOMEWORK_INDEX])
                if homeworks
                else 'Статус работы не изменился.'
            )
            if message != last_message:
                send_message(bot, message)
                last_message = message
            timestamp = response['current_date']
        except Exception as error:
            logging.error(error)
            if latest_error != error:
                message = f'Сбой в работе программы: {error}'
                send_message(bot, message)
                latest_error = error
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(
                os.path.abspath('main.log'), mode='a', encoding='UTF-8'
            ),
            logging.StreamHandler(stream=stdout),
        ],
        format='%(asctime)s [%(levelname)s] %(name)s %(message)s',
    )
    main()
