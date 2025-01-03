# Обработчик кнопки "Удалить список"

from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from models import WatchList
from bot_instance import bot
from config import DELETE_LIST_PREFIX, CONFIRM_DELETE_LIST_PREFIX, CANCEL_DELETE_LIST_PREFIX


# Обработчик кнопки "Удалить список"
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{DELETE_LIST_PREFIX}:'))
def handle_delete_list_button(call: CallbackQuery):
    """Обработчик кнопки 'Удалить список'"""
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    try:
        # Получаем список
        watchlist = WatchList.get(
            (WatchList.list_id == list_id) &
            (WatchList.user == user_id)
        )

        # Создаем клавиатуру с кнопками подтверждения
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("ДА", callback_data=f"{CONFIRM_DELETE_LIST_PREFIX}:{list_id}"),
            InlineKeyboardButton("ОТМЕНА", callback_data=f"{CANCEL_DELETE_LIST_PREFIX}:{list_id}")
        )

        # Отправляем сообщение с подтверждением
        bot.edit_message_text(
            f"Удалить список '{watchlist.name}'? Это действие невозможно отменить.",
            user_id,
            call.message.message_id,
            reply_markup=markup
        )

        bot.answer_callback_query(call.id)

    except Exception as e:
        # print(f"Error in handle_delete_list_button: {str(e)}")  # Отладка
        bot.answer_callback_query(
            call.id,
            "Ошибка при подготовке удаления списка!"
        )

