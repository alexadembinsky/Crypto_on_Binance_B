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


# Обработчик выбора списка (нажатия на список в перечне списков) - показывает список с кнопками управления
@bot.callback_query_handler(func=lambda call: call.data.startswith('show_list:'))
def handle_list_selection(call: CallbackQuery):
    """Обработчик выбора списка (нажатия на список в перечне списков) - показывает список с кнопками управления"""
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

    if len(pairs) == 0:
        pairs_text = "Список пока пуст."
    # если в списке пороговое количество пар или менее, будем получать информацию, запрашивая ее по очереди
    # для каждой пары (сколько пар в списке - столько запросов)
    elif len(pairs) <= THRESHOLD_OF_LIST_LENGTH_FOR_QUERY_MODE:
        # Получаем пары из списка и их текущие цены
        pairs_text = ""
        for pair in pairs:
            try:
                # Получаем форматированную цену и изменение
                r_o_f, price_info = BinanceAPI.format_price_change(pair.symbol)
                pairs_text += f"{r_o_f} {pair.symbol}: {price_info}\n"
            except:
                pairs_text += f"{pair.symbol}: Ошибка получения данных\n"
    # если в списке более порогового количество пар, делаем запрос без параметра, и отбираем из массива
    # полученной информации только нужные нам пары:
    else:
        # получаем список тикетов ("символов") пар:
        list_of_pairs = []
        for pair in pairs:
            list_of_pairs.append(pair.symbol)  # добавляем очередной тикет ("символ")
        #  Получаем форматированный текст с символами изменения, тикерами пар, ценой и величиной изменения
        pairs_text = ''
        try:
            pairs_text = BinanceAPI.get_pairs_with_prices_as_text(list_of_pairs)
        except:
            pairs_text += f"Ошибка получения данных для списка пар: {list_of_pairs}\n"

    bot.edit_message_text(
        f"Список: {watchlist.name}\n\n{pairs_text}",
        user_id,
        call.message.message_id,
        reply_markup=markup,
    )
    bot.answer_callback_query(call.id)


