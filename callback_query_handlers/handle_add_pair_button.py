# Обработчик кнопки "Добавить пару"

from telebot.types import CallbackQuery
from bot_instance import bot, BotStates
from config import ADD_PAIR_TO_LIST_PREFIX
from other_functions.trace_function_call import trace_function_call


# Обработчик кнопки "Добавить пару"
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{ADD_PAIR_TO_LIST_PREFIX}:'))
def handle_add_pair_button(call: CallbackQuery):
    """Обработчик кнопки 'Добавить пару'"""
    trace_function_call()
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    # Сохраняем ID списка в данных состояния
    bot.set_state(user_id, BotStates.adding_pair)
    with bot.retrieve_data(user_id) as data:
        data['list_id'] = list_id

    bot.answer_callback_query(call.id)
    bot.send_message(
        user_id,
        "Введите тикер торговой пары (например, BTCUSDT):"
    )

