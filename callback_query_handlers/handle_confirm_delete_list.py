# Обработчик подтверждения удаления списка

from telebot.types import CallbackQuery
from models import WatchList
from bot_instance import bot


# Обработчик подтверждения удаления списка
@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_delete:'))
def handle_confirm_delete_list(call: CallbackQuery):
    """Обработчик подтверждения удаления списка"""
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    try:
        # Получаем список
        watchlist = WatchList.get(
            (WatchList.list_id == list_id) &
            (WatchList.user == user_id)
        )
        list_name = watchlist.name

        # Удаляем список
        watchlist.delete_instance(recursive=True)

        # Сообщаем об успешном удалении
        bot.edit_message_text(
            f"Список '{list_name}' удален.",
            user_id,
            call.message.message_id
        )

        bot.answer_callback_query(call.id)

    except Exception as e:
        # print(f"Error in handle_confirm_delete_list: {str(e)}")  # Отладка
        bot.answer_callback_query(
            call.id,
            "Ошибка при удалении списка!"
        )

