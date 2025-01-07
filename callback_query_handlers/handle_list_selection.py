# Обработчик выбора списка (нажатия на список в перечне списков) - показывает список с кнопками управления

from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from models import WatchList
from binance_api import BinanceAPI
from bot_instance import bot
from config import (
    ADD_PAIR_TO_LIST_PREFIX,
    REMOVE_PAIR_FROM_LIST_PREFIX,
    RENAME_LIST_PREFIX,
    DELETE_LIST_PREFIX,
    REMOVE_STARTUP_PREFIX,
    ADD_STARTUP_PREFIX,
    THRESHOLD_OF_LIST_LENGTH_FOR_QUERY_MODE
)
from db_operations import get_watchlist, get_watchlist_pairs
from keyboards import get_list_actions_keyboard
from other_functions.get_pairs_info import get_pairs_info
from other_functions.trace_function_call import trace_function_call


# Обработчик выбора списка (нажатия на список в перечне списков) - показывает список с кнопками управления
@bot.callback_query_handler(func=lambda call: call.data.startswith('show_list:'))
def handle_list_selection(call: CallbackQuery):
    """Обработчик выбора списка (нажатия на список в перечне списков) - показывает список с кнопками управления"""
    trace_function_call()
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    ## Получаем выбранный список @ОБД
    #watchlist = WatchList.get_or_none(
    #    (WatchList.list_id == list_id) &
    #    (WatchList.user == user_id)
    #)
    watchlist = get_watchlist(list_id, user_id)  # получаем список или None (запрос к БД)

    if watchlist:
        try:
            pairs = get_watchlist_pairs(watchlist)
        except:
            bot.answer_callback_query(call.id, "Ошибка получения торговых пар списка")
            return
    else:
        bot.answer_callback_query(call.id, "Список не найден!")
        return

    # Создаем клавиатуру с действиями
    #markup = InlineKeyboardMarkup(row_width=2)
    #markup.add(
    #    InlineKeyboardButton("Добавить пару", callback_data=f"{ADD_PAIR_TO_LIST_PREFIX}:{list_id}"),
    #    InlineKeyboardButton("Удалить пару", callback_data=f"{REMOVE_PAIR_FROM_LIST_PREFIX}:{list_id}"),
    #    InlineKeyboardButton("Переименовать", callback_data=f"{RENAME_LIST_PREFIX}:{list_id}"),
    #    InlineKeyboardButton("Удалить список", callback_data=f"{DELETE_LIST_PREFIX}:{list_id}")
    #)
    #

    # Добавляем кнопку показа при запуске
    #if watchlist.show_on_startup:
    #    markup.add(InlineKeyboardButton(
    #        "Не показывать список при запуске",
    #        callback_data=f"{REMOVE_STARTUP_PREFIX}:{list_id}"
    #    ))
    #else:
    #    markup.add(InlineKeyboardButton(
    #        "Показывать список при запуске",
    #        callback_data=f"{ADD_STARTUP_PREFIX}:{list_id}"
    #    ))

    markup = get_list_actions_keyboard(list_id, watchlist.show_on_startup)

    # Получаем информацию о торговых парах:
    pairs_text = get_pairs_info(pairs)

    bot.edit_message_text(
        f"Список: {watchlist.name}\n\n{pairs_text}",
        user_id,
        call.message.message_id,
        reply_markup=markup,
    )
    bot.answer_callback_query(call.id)

