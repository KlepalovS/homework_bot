# Telegram-Бот ассистент для работы с API сервиса Яндекс.Домашка.
## Описание.
Данный Telegram-бот обращается к API сервиса Яндекс.Домашка и узнает статус домашней работы. Статусы домашней работы приходят в telegram-бот, студент узнает взята ли домашняя работа в ревью, проверена ли она, а если проверена - то принял ли ее ревьюер или вернул на доработку.
## Что делает бот.
 - раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
 - при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
 - логирует свою работу и сообщает о важных проблемах сообщением в Telegram.


## Используемые технологии и пакеты.
* python 3.7.9
* python-dotenv 0.19.0
* python-telegram-bot 13.7
* requests 2.26.0

## Установка.
* Клонировать проект
```
git clone https://github.com/KlepalovS/homework_bot.git
```
* Перейти в директорию homework_bot
```
cd homework_bot
```
* Создать окружение
```
python3 -m venv venv
```
* Активировать окружение
```
. venv/bin/activate
```
* Установить зависимости
```
pip3 install -r requirements.txt
```
* Создать файл .env с переменными окружения (при необходимости изменить)
```
echo PRACTICUM_TOKEN = PRACTICUM_TOKEN >> .env
echo TELEGRAM_TOKEN = TELEGRAM_TOKEN >> .env
echo TELEGRAM_CHAT_ID = TELEGRAM_CHAT_ID >> .env
```
Здесь  
PRACTICUM_TOKEN - токен [API сервиса Практикум.Домашка](https://code.s3.yandex.net/backend-developer/%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D1%83%D0%BC.%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BA%D0%B0%20%D0%A8%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0.pdf);  
TELEGRAM_TOKEN - токен [Telegram-бота](https://core.telegram.org/bots#how-do-i-create-a-bot), от чьего имени будут отправляться сообщения;  
TELEGRAM_CHAT_ID - [идентификатор Telegam-чата](https://t.me/getmyid_bot), в который будут отправляться сообщения.
* Запустить проект
```
python3 homework_bot.py
```
## Автор проекта.
Вячеслав Клепалов [ссылка на Git](https://github.com/KlepalovS).