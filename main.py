import telebot
from config import DEFAULT_COMMANDS
from models import init_db
from bot_instance import bot
from datetime import datetime
import command_handlers  # этот импорт необходим (!!!), хотя в PyCharm отображается как неактивный
import callback_query_handlers  # этот импорт необходим (!!!), хотя в PyCharm отображается как неактивный
import message_handlers  # этот импорт необходим (!!!), хотя в PyCharm отображается как неактивный


def main():
    """Основная функция запуска бота"""
    # Инициализация базы данных
    init_db()

    # Установка команд бота в меню
    bot.set_my_commands([
        telebot.types.BotCommand(command, description)
        for command, description in DEFAULT_COMMANDS
    ])

    date_and_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    date, time = date_and_time.split()
    print(f"Binance bot запущен {date} в {time}...")
    # Запуск бота
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
