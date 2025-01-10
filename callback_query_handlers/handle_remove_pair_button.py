# Обработчик кнопки "Удалить пару" под списком пар (нажатие на кнопку выводит кнопки с тикерами торговых пар
# для удаления конкретных пар)

from telebot.types import CallbackQuery
from bot_instance import bot
from config import REMOVE_SOME_PAIR_BUTTON_PREFIX
from db_operations import get_watchlist, get_watchlist_pairs
from keyboards import get_remove_pairs_keyboard
from other_functions.trace_function_call import trace_function_call


# Обработчик кнопки "Удалить пару"
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{REMOVE_SOME_PAIR_BUTTON_PREFIX}:'))
def handle_remove_pair_button(call: CallbackQuery):
    """Обработчик кнопки 'Удалить пару'"""
    trace_function_call()
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    try:
        watchlist = get_watchlist(list_id, user_id)  # получаем список @ОБД
        if not watchlist:
            bot.answer_callback_query(call.id, "Список не найден!")
            print(f'Ошибка: список не найден при получении списка при выборе опции удаления пары из списка')
            return
    except Exception as e:
        print(f'Ошибка соединения с базой данных при получении списка при выборе опции '
              f'удаления пары из списка: {str(e)}')
        bot.answer_callback_query(call.id, "Ошибка соединения с базой данных!")
        return

    try:
        pairs = get_watchlist_pairs(watchlist)  # получаем все пары для данного списка @ОБД
        if len(pairs) == 0:  # если в списке нет торговых пар
            bot.answer_callback_query(
                call.id,
                "В списке нет пар для удаления!"
            )
            return

        # Создаем клавиатуру с парами
        markup = get_remove_pairs_keyboard(list_id, pairs)  # @IK

        bot.edit_message_text(
            "Выберите пару для удаления:",
            user_id,
            call.message.message_id,
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f'Ошибка соединения с базой данных при получении всех пар для данного списка: {str(e)} ')
        bot.answer_callback_query(call.id, "Ошибка соединения с базой данных!")

