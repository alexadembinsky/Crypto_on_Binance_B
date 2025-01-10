# Обработчик кнопки "Удалить список"

from telebot.types import CallbackQuery
from bot_instance import bot
from config import DELETE_LIST_PREFIX
from db_operations import get_watchlist
from keyboards import get_confirm_delete_list_keyboard
from other_functions.trace_function_call import trace_function_call


# Обработчик кнопки "Удалить список"
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{DELETE_LIST_PREFIX}:'))
def handle_delete_list_button(call: CallbackQuery):
    """Обработчик кнопки 'Удалить список'"""
    trace_function_call()
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    try:
        # Получаем список
        watchlist = get_watchlist(list_id, user_id)  # @ОБД

        # Создаем клавиатуру с кнопками подтверждения
        markup = get_confirm_delete_list_keyboard(list_id)  # @IK

        # Отправляем сообщение с подтверждением
        bot.edit_message_text(
            f"Удалить список '{watchlist.name}'? Это действие невозможно отменить.",
            user_id,
            call.message.message_id,
            reply_markup=markup
        )

        bot.answer_callback_query(call.id)

    except Exception as e:
        print(f"Ошибка при выборе опции удаления списка: {str(e)}")  # error message
        bot.answer_callback_query(
            call.id,
            "Ошибка при подготовке удаления списка!"
        )

