# Обработчик завершения добавления пар в список / кнопки "Завершить редактирование списка"

from telebot.types import CallbackQuery
from bot_instance import bot
import callback_query_handlers
from config import LIST_COMPLETE
from db_operations import get_watchlist


# Обработчик завершения добавления пар в список / кнопки "Завершить редактирование списка"
@bot.callback_query_handler(func=lambda call: call.data == f"{LIST_COMPLETE}")
def handle_list_complete(call: CallbackQuery):
    """Обработчик завершения добавления пар в список / кнопки "Завершить редактирование списка" """

    user_id = call.from_user.id

    # Получаем ID списка из состояния
    with bot.retrieve_data(user_id) as data:
        list_id = data.get('list_id')

    # Находим список по ID и ID пользователя
    watchlist = get_watchlist(list_id, user_id)

    if watchlist:
        # Модифицируем текущий callback
        call.data = f"show_list:{watchlist.list_id}"

        # Вызываем handle_list_selection с модифицированным callback
        callback_query_handlers.handle_list_selection(call)

        # Сбрасываем состояние после завершения
        bot.delete_state(user_id)

        # Отвечаем на исходный callback
        bot.answer_callback_query(call.id)
    else:
        bot.answer_callback_query(call.id, "Список не найден")

