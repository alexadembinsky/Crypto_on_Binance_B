# Обработчик ввода нового названия списка

from telebot.types import Message
from models import WatchList
from bot_instance import bot, BotStates
from db_operations import get_watchlist, rename_watchlist


# Обработчик ввода нового названия списка
@bot.message_handler(state=BotStates.renaming_list)
def process_rename_list(message: Message):
    """Обработчик ввода нового названия списка"""
    user_id = message.from_user.id
    new_name = message.text.strip()

    # Проверяем длину названия
    if len(new_name) < 1 or len(new_name) > 50:
        bot.send_message(
            user_id,
            "Название должно быть от 1 до 50 символов. Попробуйте ещё раз:"
        )
        return  # Выходим из функции, состояние сохранится

    try:
        # Получаем ID списка из данных состояния
        with bot.retrieve_data(user_id) as data:
            list_id = data['list_id']

        # Получаем список
        watchlist = get_watchlist(list_id, user_id)  # @ОБД
        if not watchlist:
            bot.send_message(user_id, "Список не найден")
            bot.delete_state(user_id)
            return

        old_name = watchlist.name

        # Пробуем переименовать список
        rename_watchlist(watchlist, new_name)  # @ОБД

        # Если мы дошли до этой строки, значит переименование прошло успешно
        bot.send_message(
            user_id,
            f"Список '{old_name}' переименован в '{new_name}'!"
        )
        bot.delete_state(user_id)

    except Exception as e:
        print(f'Функция process_rename_list(): Произошла непредвиденная ошибка: {e}')
        bot.send_message(
            user_id,
            f"Произошла непредвиденная ошибка: {e}"
        )
        bot.delete_state(user_id)

