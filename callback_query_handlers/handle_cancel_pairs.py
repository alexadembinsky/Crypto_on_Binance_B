# Обработчик кнопки 'НЕТ' для отказа от показа найденных торговых пар

from telebot.types import CallbackQuery
from bot_instance import bot


# Обработчик кнопки 'НЕТ' для отказа от показа найденных торговых пар
@bot.callback_query_handler(func=lambda call: call.data == 'cancel_pairs')
def handle_cancel_pairs(call: CallbackQuery):
    """Обработчик кнопки 'НЕТ' для отказа от показа найденных торговых пар"""
    # Просто удаляем сообщение с кнопками
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    bot.delete_state(call.from_user.id)  # Удаляем состояние
    bot.answer_callback_query(call.id)
