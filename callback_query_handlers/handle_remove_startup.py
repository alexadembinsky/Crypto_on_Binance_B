# Обработчик отмены показа списка при запуске

from telebot.types import CallbackQuery
from bot_instance import bot
import callback_query_handlers
from config import REMOVE_STARTUP_PREFIX
from db_operations import disable_startup_list
from other_functions.trace_function_call import trace_function_call


# Обработчик отмены показа списка при запуске
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{REMOVE_STARTUP_PREFIX}:'))
def handle_remove_startup(call: CallbackQuery):
    """Обработчик отмены показа списка при запуске"""
    trace_function_call()
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    success, message = disable_startup_list(list_id, user_id)  # Обращаемся к БД @ОБД

    bot.answer_callback_query(call.id, message)

    if success:
        # Обновляем отображение списка
        new_call = call
        new_call.data = f"show_list:{list_id}"
        callback_query_handlers.handle_list_selection(new_call)
