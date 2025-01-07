# Обработчик добавления показа списка при запуске

from telebot.types import CallbackQuery
from models import WatchList
from bot_instance import bot
import callback_query_handlers
from config import ADD_STARTUP_PREFIX, SHOW_LIST_PREFIX
from db_operations import set_startup_list, get_watchlist_name
from other_functions.trace_function_call import trace_function_call


# Обработчик добавления показа списка при запуске
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{ADD_STARTUP_PREFIX}:'))
def handle_add_startup(call: CallbackQuery):
    """Обработчик добавления показа списка при запуске"""
    trace_function_call()
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    try:
        # @ОБД
        ## Сначала убираем флаг у всех списков пользователя
        #WatchList.update(show_on_startup=False).where(
        #    WatchList.user == user_id
        #).execute()

        ## Устанавливаем флаг для выбранного списка
        #watchlist = WatchList.get(
        #    (WatchList.list_id == list_id) &
        #    (WatchList.user == user_id)
        #)
        #watchlist.show_on_startup = True
        #watchlist.save()
        set_startup_list(user_id, list_id)  # устанавливаем флаг показа у листа с данным id

        # Выводим сообщение:
        bot.answer_callback_query(
            call.id,
            f"Список '{get_watchlist_name(list_id, user_id)}' будет выводиться при запуске бота"
        )

        # Обновляем отображение списка
        new_call = call
        new_call.data = f"{SHOW_LIST_PREFIX}:{list_id}"
        callback_query_handlers.handle_list_selection(new_call)

    except Exception as e:
        # print(f"Error in handle_add_startup: {str(e)}")  # Отладка
        bot.answer_callback_query(
            call.id,
            "Ошибка при установке показа списка при запуске!"
        )

