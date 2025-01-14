# Обработчик завершения добавления пар в список / кнопки "Завершить редактирование списка"

from telebot.types import CallbackQuery
from bot_instance import bot
import callback_query_handlers
from config import LIST_COMPLETE
from db_operations import get_watchlist
from other_functions.trace_function_call import trace_function_call


# Обработчик завершения добавления пар в список / кнопки "Завершить редактирование списка"
@bot.callback_query_handler(func=lambda call: call.data == f"{LIST_COMPLETE}")
def handle_list_complete(call: CallbackQuery):
    """Обработчик завершения добавления пар в список / кнопки "Завершить редактирование списка" """
    trace_function_call()

    user_id = call.from_user.id

    # Получаем ID списка из состояния
    with bot.retrieve_data(user_id) as data:
        list_id = data.get('list_id')

    try:
        # Находим список по ID списка и ID пользователя
        watchlist = get_watchlist(list_id, user_id)  # @ОБД

        if watchlist:  # если список найден, и функция get_watchlist() вернула не None
            # Модифицируем текущий callback
            call.data = f"show_list:{watchlist.list_id}"

            # Вызываем handle_list_selection с модифицированным callback
            callback_query_handlers.handle_list_selection(call)

            # Сбрасываем состояние после завершения
            bot.delete_state(user_id)

            # Отвечаем на исходный callback
            bot.answer_callback_query(call.id)
        else:  # если список не найден, т. е. функция get_watchlist() вернула None
            bot.answer_callback_query(call.id, "Не удается завершить редактирование - список не найден")
            print(f'Ошибка: не удалось получить список из базы данных при попытке завершения редактирования. '
                  f'Функция get_watchlist() вернула None')
    except Exception as e:
        print(f'Ошибка соединения с базой данных при попытке завершения редактирования списка: {str(e)}')
        bot.answer_callback_query(call.id, "Ошибка базы данных. Не удается завершить редактирование списка")


