# Обработчик выбора списка (нажатия на список в перечне списков) - показывает список с кнопками управления

from telebot.types import CallbackQuery
from bot_instance import bot
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

    try:
        # Получаем выбранный список
        watchlist = get_watchlist(list_id, user_id)  # получаем список или None (запрос к БД) @ОБД
        if watchlist:  # если мы получили список (ответ был не None)
            try:
                pairs = get_watchlist_pairs(watchlist)  # получаем все пары списка

                # Создаем клавиатуру с действиями
                markup = get_list_actions_keyboard(list_id, watchlist.show_on_startup)  # @IK

                # Получаем информацию о торговых парах в виде форматированного текста:
                pairs_text = get_pairs_info(pairs)

                # Выводим список с заголовком и клавиатурой
                bot.edit_message_text(
                    f"<b>{watchlist.name}</b>\n{pairs_text}",
                    user_id,
                    call.message.message_id,
                    reply_markup=markup,
                    parse_mode='HTML'
                )
                bot.answer_callback_query(call.id)

            except Exception as e:
                bot.answer_callback_query(call.id, "Ошибка получения торговых пар списка")
                print(f'Ошибка при получении всех торговых пар списка: {str(e)}')
                return
        else:  # если мы не получили список (ответ был None)
            bot.answer_callback_query(call.id, "Список не найден!")
            print(f'Ошибка: список не найден при нажатии на список (кнопку с названием списка) в перечне списков')
            return

    except Exception as e:
        print(f'Ошибка соединения с БД: не удалось получить список')  # error message
        bot.answer_callback_query(call.id, "Не удалось получить список")

