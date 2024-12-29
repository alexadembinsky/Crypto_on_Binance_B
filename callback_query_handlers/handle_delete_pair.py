# обработчик выбора пары для удаления из списка
# (обработчик кнопки с тикером торговой пары, нажатие на которую приводит к удалению торговой пары из списка)

from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from models import User, init_db, WatchList, TradingPair
from bot_instance import bot, BotStates
import callback_query_handlers
from config import DELETE_THE_PAIR_PREFIX


# обработчик выбора пары для удаления
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{DELETE_THE_PAIR_PREFIX}:'))
def handle_delete_pair(call: CallbackQuery):
    """Обработчик выбора пары для удаления"""
    user_id = call.from_user.id

    try:
        parts = call.data.split(':')
        if len(parts) != 3:
            bot.answer_callback_query(
                call.id,
                "Ошибка формата данных"
            )
            return

        list_id = int(parts[1])
        pair_id = int(parts[2])

        # Получаем пару, проверяя принадлежность пользователю через watchlist
        pair = (TradingPair
                .select()
                .join(WatchList)
                .where(
            (TradingPair.pair_id == pair_id) &
            (WatchList.user == user_id)
        )
                .get())

        symbol = pair.symbol
        pair.delete_instance()

        bot.answer_callback_query(
            call.id,
            f"Пара {symbol} удалена из списка!"
        )

        # Возвращаемся к просмотру списка
        new_call = call
        new_call.data = f"show_list:{list_id}"
        callback_query_handlers.handle_list_selection(new_call)

    except (ValueError, IndexError):
        bot.answer_callback_query(
            call.id,
            "Ошибка в формате данных кнопки"
        )
    except Exception as e:
        # print(f"Error in handle_delete_pair: {str(e)}")  # Отладка
        bot.answer_callback_query(
            call.id,
            "Ошибка при удалении пары!"
        )
