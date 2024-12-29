# Обработчик добавления показа списка при запуске

from telebot.types import CallbackQuery
from models import WatchList
from bot_instance import bot
import callback_query_handlers


# Обработчик добавления показа списка при запуске
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_startup:'))
def handle_add_startup(call: CallbackQuery):
    """Обработчик добавления показа списка при запуске"""
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    try:
        # Сначала убираем флаг у всех списков пользователя
        WatchList.update(show_on_startup=False).where(
            WatchList.user == user_id
        ).execute()

        # Устанавливаем флаг для выбранного списка
        watchlist = WatchList.get(
            (WatchList.list_id == list_id) &
            (WatchList.user == user_id)
        )
        watchlist.show_on_startup = True
        watchlist.save()

        bot.answer_callback_query(
            call.id,
            f"Список '{watchlist.name}' будет выводиться при запуске бота"
        )

        # Обновляем отображение списка
        new_call = call
        new_call.data = f"show_list:{list_id}"
        callback_query_handlers.handle_list_selection(new_call)

    except Exception as e:
        # print(f"Error in handle_add_startup: {str(e)}")  # Отладка
        bot.answer_callback_query(
            call.id,
            "Ошибка при установке показа списка при запуске!"
        )

