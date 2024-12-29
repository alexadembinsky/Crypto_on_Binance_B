# Обработчик текстовых сообщений как запросов тикера

from telebot.types import Message
from other_functions import is_valid_ticker_request, process_price_request_direct
from bot_instance import bot, BotStates


# Обработчик текстовых сообщений как запросов тикера
@bot.message_handler(func=lambda message: True)
def handle_text(message: Message):
    """Обработчик текстовых сообщений как запросов тикера"""
    # print('Запущен обработчик "просто" текстовых сообщений handle_text') # Отладка
    # Проверяем, не находится ли пользователь в каком-либо состоянии
    if bot.get_state(message.from_user.id):
        return  # Если да, позволяем другим обработчикам обработать сообщение

    text = message.text.strip()
    if not text:
        return

    # Разбиваем текст по пробелам
    parts = text.split()
    potential_ticker = parts[0].upper()

    # Проверяем первое слово на валидность
    if not is_valid_ticker_request(potential_ticker):
        bot.reply_to(message, "Введите тикер или команду")
        return

    # Если сообщение содержит более одного слова, проверяем только первое
    if len(parts) > 1:
        # Обрабатываем первое слово как тикер
        process_price_request_direct(message, potential_ticker)
    else:
        # Если сообщение состоит из одного слова, обрабатываем его целиком
        process_price_request_direct(message, text.upper())


