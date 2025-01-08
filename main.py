import telebot
from config import DEFAULT_COMMANDS
from models import init_db
from bot_instance import bot
from datetime import datetime
from time import sleep
import signal
import sys
import command_handlers  # этот импорт необходим (!!!), хотя в PyCharm отображается как неактивный
import callback_query_handlers  # этот импорт необходим (!!!), хотя в PyCharm отображается как неактивный
import message_handlers  # этот импорт необходим (!!!), хотя в PyCharm отображается как неактивный


def signal_handler(sig, frame):
    print('\nЗавершение работы бота...')
    bot.stop_polling()
    date, time = print_date_and_time()
    print(f'Binance bot остановлен {date} в {time}.')
    sys.exit(0)


def print_date_and_time():
    """Функция вывода текущих даты и времени как кортежа"""
    date_and_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    return date_and_time.split()


def main():
    """Основная функция запуска бота"""
    # Регистрируем обработчик сигнала завершения
    signal.signal(signal.SIGINT, signal_handler)

    # Инициализация базы данных
    init_db()

    # Установка команд бота в меню
    bot.set_my_commands([
        telebot.types.BotCommand(command, description)
        for command, description in DEFAULT_COMMANDS
    ])

    # Бесконечный цикл работы бота с обработкой исключений
    while True:
        try:
            date, time = print_date_and_time()  # Вывод времени при каждом запуске/перезапуске
            print(f"Binance bot запущен {date} в {time}...")
            bot.infinity_polling(timeout=15, allowed_updates=["message", "callback_query"])
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            sleep(15)  # Пауза перед перезапуском


if __name__ == '__main__':
    main()
