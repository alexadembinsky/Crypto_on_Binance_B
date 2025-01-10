# Обработчик кнопки 'ДА' для показа всех найденных торговых пар

from telebot.types import CallbackQuery
from bot_instance import bot
from other_functions import show_pairs_info
from config import SHOW_PAIRS
from other_functions.trace_function_call import trace_function_call


# Обработчик кнопки 'ДА' для показа всех найденных торговых пар
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{SHOW_PAIRS}:'))
def handle_show_pairs(call: CallbackQuery):
    """Обработчик кнопки 'ДА' для показа всех найденных пар"""
    trace_function_call()
    user_id = call.from_user.id

    # Сразу отвечаем на callback query
    bot.answer_callback_query(call.id)

    with bot.retrieve_data(user_id) as data:
        matched_pairs = data.get('matched_pairs', [])

    # Удаляем сообщение с кнопками
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )

    # Показываем пары
    show_pairs_info(user_id, matched_pairs)
    bot.delete_state(user_id)

