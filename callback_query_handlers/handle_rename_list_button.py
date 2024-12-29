# Обработчик кнопки "Переименовать список"

from telebot.types import CallbackQuery
from bot_instance import bot, BotStates
from config import RENAME_LIST_PREFIX


# Обработчик кнопки "Переименовать список"
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{RENAME_LIST_PREFIX}:'))
def handle_rename_list_button(call: CallbackQuery):
    """Обработчик кнопки 'Переименовать список'"""
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    # Сохраняем ID списка в данных состояния
    bot.set_state(user_id, BotStates.renaming_list)
    with bot.retrieve_data(user_id) as data:
        data['list_id'] = list_id

    bot.answer_callback_query(call.id)
    bot.send_message(
        user_id,
        "Введите новое название для списка:"
    )
