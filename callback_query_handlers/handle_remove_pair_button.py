# Обработчик кнопки "Удалить пару" под списком пар (нажатие на кнопку выводит кнопки с тикерами торговых пар
# для удаления конкретных пар)

from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot_instance import bot
from config import REMOVE_SOME_PAIR_BUTTON_PREFIX
from db_operations import get_watchlist, get_pairs_count, get_watchlist_pairs
from keyboards import get_remove_pairs_keyboard
from other_functions.trace_function_call import trace_function_call


# Обработчик кнопки "Удалить пару"
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{REMOVE_SOME_PAIR_BUTTON_PREFIX}:'))
def handle_remove_pair_button(call: CallbackQuery):
    """Обработчик кнопки 'Удалить пару'"""
    trace_function_call()
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    # @ОБД
    #watchlist = WatchList.get_or_none(
    #    (WatchList.list_id == list_id) &
    #    (WatchList.user == user_id)
    #)
    watchlist = get_watchlist(list_id, user_id)  # получаем список @ОБД
    if not watchlist:
        bot.answer_callback_query(
            call.id,
            "Список не найден!"
        )
        return

    pairs = get_watchlist_pairs(watchlist)  # получаем все пары для данного списка @ОБД
    if len(pairs) == 0:  # если в списке нет торговых пар
        bot.answer_callback_query(
            call.id,
            "В списке нет пар для удаления!"
        )
        return

    # Создаем клавиатуру с парами @IK
    #markup = InlineKeyboardMarkup()
    #for pair in pairs:
    #    markup.add(InlineKeyboardButton(
    #        pair.symbol,
    #        callback_data=f"delete_pair:{list_id}:{pair.pair_id}"
    #    ))
    #markup.add(InlineKeyboardButton(
    #    "↩️ Назад",
    #    callback_data=f"show_list:{list_id}"
    #))
    markup = get_remove_pairs_keyboard(list_id, pairs)

    bot.edit_message_text(
        "Выберите пару для удаления:",
        user_id,
        call.message.message_id,
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

