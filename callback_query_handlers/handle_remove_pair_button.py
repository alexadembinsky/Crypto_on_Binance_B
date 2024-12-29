# Обработчик кнопки "Удалить пару" под списком пар (нажатие на кнопку выводит кнопки с тикерами торговых пар
# для удаления конкретных пар)

from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from models import WatchList
from bot_instance import bot
from config import REMOVE_SOME_PAIR_BUTTON_PREFIX


# Обработчик кнопки "Удалить пару"
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{REMOVE_SOME_PAIR_BUTTON_PREFIX}:'))
def handle_remove_pair_button(call: CallbackQuery):
    """Обработчик кнопки 'Удалить пару'"""
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    watchlist = WatchList.get_or_none(
        (WatchList.list_id == list_id) &
        (WatchList.user == user_id)
    )

    if not watchlist or not watchlist.pairs.count():
        bot.answer_callback_query(
            call.id,
            "В списке нет пар для удаления!"
        )
        return

    # Создаем клавиатуру с парами
    markup = InlineKeyboardMarkup()
    for pair in watchlist.pairs:
        markup.add(InlineKeyboardButton(
            pair.symbol,
            callback_data=f"delete_pair:{list_id}:{pair.pair_id}"
        ))
    markup.add(InlineKeyboardButton(
        "↩️ Назад",
        callback_data=f"show_list:{list_id}"
    ))

    bot.edit_message_text(
        "Выберите пару для удаления:",
        user_id,
        call.message.message_id,
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

