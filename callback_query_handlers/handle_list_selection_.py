# Обработчик выбора списка (нажатия на список в перечне списков) - показывает список с кнопками управления

from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from models import WatchList
from binance_api import BinanceAPI
from bot_instance import bot


# Обработчик выбора списка (нажатия на список в перечне списков) - показывает список с кнопками управления
@bot.callback_query_handler(func=lambda call: call.data.startswith('show_list:'))
def handle_list_selection(call: CallbackQuery):
    """Обработчик выбора списка (нажатия на список в перечне списков) - показывает список с кнопками управления"""
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    # Получаем выбранный список
    watchlist = WatchList.get_or_none(
        (WatchList.list_id == list_id) &
        (WatchList.user == user_id)
    )

    if not watchlist:
        bot.answer_callback_query(call.id, "Список не найден!")
        return

    # Создаем клавиатуру с действиями
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Добавить пару", callback_data=f"add_pair:{list_id}"),
        InlineKeyboardButton("Удалить пару", callback_data=f"remove_pair:{list_id}"),
        InlineKeyboardButton("Переименовать", callback_data=f"rename_list:{list_id}"),
        InlineKeyboardButton("Удалить список", callback_data=f"delete_list:{list_id}")
    )

    # Добавляем кнопку показа при запуске
    if watchlist.show_on_startup:
        markup.add(InlineKeyboardButton(
            "Не показывать список при запуске",
            callback_data=f"remove_startup:{list_id}"
        ))
    else:
        markup.add(InlineKeyboardButton(
            "Показывать список при запуске",
            callback_data=f"add_startup:{list_id}"
        ))

    # Получаем пары из списка и их текущие цены
    pairs_text = ""
    for pair in watchlist.pairs:
        try:
            # Получаем форматированную цену и изменение
            r_o_f, price_info = BinanceAPI.format_price_change(pair.symbol)
            pairs_text += f"{r_o_f} {pair.symbol}: {price_info}\n"
        except Exception as e:
            pairs_text += f"{pair.symbol}: Ошибка получения данных\n"

    if not watchlist.pairs.count():
        pairs_text = "Список пока пуст."

    bot.edit_message_text(
        f"Список: {watchlist.name}\n\n{pairs_text}",
        user_id,
        call.message.message_id,
        reply_markup=markup,
    )
    bot.answer_callback_query(call.id)


