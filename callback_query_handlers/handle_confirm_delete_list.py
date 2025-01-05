# Обработчик подтверждения удаления списка

from telebot.types import CallbackQuery
from models import WatchList
from bot_instance import bot
from config import CONFIRM_DELETE_LIST_PREFIX
from db_operations import delete_watchlist, get_watchlist_name


# Обработчик подтверждения удаления списка
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{CONFIRM_DELETE_LIST_PREFIX}:'))
def handle_confirm_delete_list(call: CallbackQuery):
    """Обработчик подтверждения удаления списка"""
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    try:
        # Получаем список @ОБД
        #watchlist = WatchList.get(
        #    (WatchList.list_id == list_id) &
        #    (WatchList.user == user_id)
        #)
        #list_name = watchlist.name

        ## Удаляем список
        #watchlist.delete_instance(recursive=True)
        watchlist_name = get_watchlist_name(list_id, user_id)
        delete_watchlist(list_id, user_id)
        # Сообщаем об успешном удалении
        bot.edit_message_text(
            f"Список '{watchlist_name}' удален.",
            user_id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)

    except Exception as e:
        # print(f"Error in handle_confirm_delete_list: {str(e)}")  # Отладка
        bot.answer_callback_query(
            call.id,
            "Ошибка при удалении списка!"
        )

