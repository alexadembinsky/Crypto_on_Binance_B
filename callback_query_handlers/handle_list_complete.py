# Обработчик завершения добавления пар в список / кнопки "Завершить редактирование списка"

from telebot.types import CallbackQuery
from models import WatchList
from bot_instance import bot
import callback_query_handlers


# Обработчик завершения добавления пар в список / кнопки "Завершить редактирование списка"
@bot.callback_query_handler(func=lambda call: call.data == "list_complete")
def handle_list_complete(call: CallbackQuery):
    """Обработчик завершения добавления пар в список / кнопки "Завершить редактирование списка" """

    # Получаем ID списка из предыдущего сообщения
    message_text = call.message.text
    list_name = message_text.split("'")[1]  # Получаем название списка между кавычками

    # Находим список по имени и ID пользователя
    watchlist = WatchList.get(
        (WatchList.name == list_name) &
        (WatchList.user == call.from_user.id)
    )

    # Модифицируем текущий callback
    call.data = f"show_list:{watchlist.list_id}"

    # Вызываем handle_list_selection с модифицированным callback
    callback_query_handlers.handle_list_selection(call)

    # Отвечаем на исходный callback
    bot.answer_callback_query(call.id)
