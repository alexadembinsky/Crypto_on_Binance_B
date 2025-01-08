import telebot
from config import DEFAULT_COMMANDS
from models import init_db
from bot_instance import bot
from datetime import datetime
from time import sleep
import command_handlers  # этот импорт необходим (!!!), хотя в PyCharm отображается как неактивный
import callback_query_handlers  # этот импорт необходим (!!!), хотя в PyCharm отображается как неактивный
import message_handlers  # этот импорт необходим (!!!), хотя в PyCharm отображается как неактивный


def print_startup_time():
    """Функция вывода времени запуска"""
    date_and_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    date, time = date_and_time.split()
    print(f"Binance bot запущен {date} в {time}...")


def main():
    """Основная функция запуска бота"""
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
            print_startup_time()  # Вывод времени при каждом запуске/перезапуске
            bot.infinity_polling(timeout=15)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            sleep(15)  # Пауза перед перезапуском


if __name__ == '__main__':
    main()
