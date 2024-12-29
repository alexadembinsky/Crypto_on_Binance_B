# Обработчик отмены показа списка при запуске

from telebot.types import CallbackQuery
from models import WatchList
from bot_instance import bot
import callback_query_handlers


# Обработчик отмены показа списка при запуске
@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_startup:'))
def handle_remove_startup(call: CallbackQuery):
    """Обработчик отмены показа списка при запуске"""
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    try:
        watchlist = WatchList.get(
            (WatchList.list_id == list_id) &
            (WatchList.user == user_id)
        )
        watchlist.show_on_startup = False
        watchlist.save()

        bot.answer_callback_query(
            call.id,
            f"Показ списка '{watchlist.name}' при запуске отменен"
        )

        # Обновляем отображение списка
        new_call = call
        new_call.data = f"show_list:{list_id}"
        callback_query_handlers.handle_list_selection(new_call)

    except Exception as e:
        # print(f"Error in handle_remove_startup: {str(e)}")  # Отладка
        bot.answer_callback_query(
            call.id,
            "Ошибка при отмене показа при запуске!"
        )
