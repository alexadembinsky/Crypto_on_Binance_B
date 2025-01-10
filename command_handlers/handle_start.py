# Обработчик команды /start

from peewee import IntegrityError, OperationalError, DatabaseError, InterfaceError
from bot_instance import bot
from db_operations import (create_user, create_watchlist, create_trading_pair,
                           get_startup_list, get_watchlist_pairs)
from other_functions.get_pairs_info import get_pairs_info
from other_functions.trace_function_call import trace_function_call


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    """Обработчик команды /start"""
    trace_function_call()
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        # Создаем нового пользователя и сохраняем результат в переменную @ОДБ
        new_user = create_user(user_id, username, first_name, last_name)

        # Создаем базовый список для нового пользователя @ОДБ
        base_list = create_watchlist(new_user, "Base", show_on_startup=True)

        # Добавляем базовые пары @ОБД
        for symbol in ["BTCUSDT", "ETHUSDT"]:
            create_trading_pair(base_list, symbol)  # @ОБД

        welcome_text = (
            f"Привет, {first_name}! 👋\n\n"
            "Я бот для отслеживания цены спотовых активов на бирже Binance.\n"
            "Используйте /help для просмотра доступных команд."
        )
    except IntegrityError:
        # Пользователь уже существует
        text = (
            f"С возвращением, {first_name}! 👋\n"
            "Используйте /help для просмотра доступных команд."
        )
        bot.reply_to(message, text)

    except (OperationalError, DatabaseError, InterfaceError) as e:
        text = f"Не удалось подключиться к БД: {e}"
        print(f'Ошибка соединения с базой данных: {str(e)}')
        bot.reply_to(message, "Не удалось подключиться к базе данных")

    # Проверяем наличие списка для показа при запуске
    startup_list = get_startup_list(user_id)  # @ОБД
    pairs = get_watchlist_pairs(startup_list)  # @ОБД
    if len(pairs) > 0:
        pairs_text = get_pairs_info(pairs)  # @API req

        if pairs_text:
            bot.send_message(user_id, pairs_text)

