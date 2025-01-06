from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import (ADD_PAIR_TO_LIST_PREFIX, REMOVE_PAIR_FROM_LIST_PREFIX,
                    RENAME_LIST_PREFIX, DELETE_LIST_PREFIX, CONFIRM_DELETE_LIST_PREFIX,
                    CANCEL_DELETE_LIST_PREFIX, REMOVE_STARTUP_PREFIX, ADD_STARTUP_PREFIX)
from db_operations import get_pairs_count
from other_functions.rus_number_agreement import rus_number_agreement


def get_confirm_delete_list_keyboard(list_id):
    """Клавиатура подтверждения удаления списка"""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("ДА", callback_data=f"{CONFIRM_DELETE_LIST_PREFIX}:{list_id}"),
        InlineKeyboardButton("ОТМЕНА", callback_data=f"{CANCEL_DELETE_LIST_PREFIX}:{list_id}")
    )
    return markup


def get_list_actions_keyboard(list_id, show_on_startup=False):
    """Клавиатура действий со списком"""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Добавить пару", callback_data=f"{ADD_PAIR_TO_LIST_PREFIX}:{list_id}"),
        InlineKeyboardButton("Удалить пару", callback_data=f"{REMOVE_PAIR_FROM_LIST_PREFIX}:{list_id}"),
        InlineKeyboardButton("Переименовать", callback_data=f"{RENAME_LIST_PREFIX}:{list_id}"),
        InlineKeyboardButton("Удалить список", callback_data=f"{DELETE_LIST_PREFIX}:{list_id}")
    )

    # Кнопка показа при запуске
    if show_on_startup:
        markup.add(InlineKeyboardButton(
            "Не показывать список при запуске",
            callback_data=f"{REMOVE_STARTUP_PREFIX}:{list_id}"
        ))
    else:
        markup.add(InlineKeyboardButton(
            "Показывать список при запуске",
            callback_data=f"{ADD_STARTUP_PREFIX}:{list_id}"
        ))
    return markup


def get_remove_pairs_keyboard(list_id, pairs):
    """Клавиатура для удаления пар"""
    markup = InlineKeyboardMarkup()
    for pair in pairs:
        markup.add(InlineKeyboardButton(
            pair.symbol,
            callback_data=f"delete_pair:{list_id}:{pair.pair_id}"
        ))
    markup.add(InlineKeyboardButton(
        "↩️ Назад",
        callback_data=f"show_list:{list_id}"
    ))
    return markup


def get_watchlists_keyboard(watchlists):
    """Клавиатура со списками"""
    markup = InlineKeyboardMarkup()
    for wlist in watchlists:
        pairs_count = get_pairs_count(wlist)
        eye_icon = " 👁" if wlist.show_on_startup else ""
        markup.add(InlineKeyboardButton(
            f"{wlist.name}{eye_icon} ({rus_number_agreement('', pairs_count, 'пара')})",
            callback_data=f"show_list:{wlist.list_id}"
        ))
    return markup


def get_add_more_pair_keyboard(list_id):
    """Клавиатура добавления дополнительных пар"""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Добавить ещё пару", callback_data=f"add_pair:{list_id}"),
        InlineKeyboardButton("Завершить редактирование списка", callback_data="list_complete")
    )
    return markup


def get_new_list_actions_keyboard(list_id):
    """Клавиатура действий для нового списка"""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Добавить пару", callback_data=f"add_pair:{list_id}"),
        InlineKeyboardButton("Переименовать", callback_data=f"rename_list:{list_id}"),
        InlineKeyboardButton("Удалить список", callback_data=f"delete_list:{list_id}")
    )
    return markup


def get_show_many_pairs_confirmation_keyboard(symbol):
    """Клавиатура подтверждения показа всех найденных пар"""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("ДА", callback_data=f"show_pairs:{symbol}"),
        InlineKeyboardButton("НЕТ", callback_data="cancel_pairs")
    )
    return markup
