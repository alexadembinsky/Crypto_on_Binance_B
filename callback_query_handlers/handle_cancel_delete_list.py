# Обработчик отмены удаления списка

from telebot.types import CallbackQuery
from bot_instance import bot
import callback_query_handlers


# Обработчик отмены удаления списка
@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel_delete:'))
def handle_cancel_delete_list(call: CallbackQuery):
    """Обработчик отмены удаления списка"""
    try:
        # Просто возвращаемся к просмотру списка
        list_id = int(call.data.split(':')[1])
        new_call = call
        new_call.data = f"show_list:{list_id}"
        callback_query_handlers.handle_list_selection(new_call)

        bot.answer_callback_query(call.id)

    except Exception as e:
        # print(f"Error in handle_cancel_delete_list: {str(e)}") # Отладка
        bot.answer_callback_query(
            call.id,
            "Ошибка при отмене удаления!"
        )

