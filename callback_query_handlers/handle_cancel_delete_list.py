# Обработчик отмены удаления списка

from telebot.types import CallbackQuery
from bot_instance import bot
import callback_query_handlers
from config import CANCEL_DELETE_LIST_PREFIX, SHOW_LIST_PREFIX
from other_functions.trace_function_call import trace_function_call


# Обработчик отмены удаления списка
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{CANCEL_DELETE_LIST_PREFIX}:'))
def handle_cancel_delete_list(call: CallbackQuery):
    """Обработчик отмены удаления списка"""
    trace_function_call()
    try:
        # Просто возвращаемся к просмотру списка
        list_id = int(call.data.split(':')[1])
        new_call = call
        new_call.data = f"{SHOW_LIST_PREFIX}:{list_id}"
        callback_query_handlers.handle_list_selection(new_call)

        bot.answer_callback_query(call.id)

    except Exception as e:
        print(f"Ошибка при отмене удаления списка: {str(e)}")  # error message
        bot.answer_callback_query(
            call.id,
            "Ошибка при отмене удаления!"
        )

