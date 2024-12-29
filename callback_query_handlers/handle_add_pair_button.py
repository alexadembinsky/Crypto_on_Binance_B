# Обработчик кнопки "Добавить пару"

from telebot.types import CallbackQuery
from bot_instance import bot, BotStates


# Обработчик кнопки "Добавить пару"
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_pair:'))
def handle_add_pair_button(call: CallbackQuery):
    """Обработчик кнопки 'Добавить пару'"""
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

