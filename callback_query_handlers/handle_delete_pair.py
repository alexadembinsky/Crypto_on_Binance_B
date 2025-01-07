# обработчик выбора пары для удаления из списка
# (обработчик кнопки с тикером торговой пары, нажатие на которую приводит к удалению торговой пары из списка)

from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from models import User, init_db, WatchList, TradingPair
from bot_instance import bot, BotStates
import callback_query_handlers
from config import DELETE_THE_PAIR_PREFIX
from db_operations import get_pair_symbol, delete_trading_pair
from other_functions.trace_function_call import trace_function_call


# обработчик выбора пары для удаления
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{DELETE_THE_PAIR_PREFIX}:'))
def handle_delete_pair(call: CallbackQuery):
    """Обработчик выбора пары для удаления"""
    trace_function_call()
    user_id = call.from_user.id

    parts = call.data.split(':')
    if len(parts) != 3:
        bot.answer_callback_query(call.id, "Ошибка формата данных")
        return

    list_id = int(parts[1])
    pair_id = int(parts[2])

    try:
        # Получаем пару, проверяя принадлежность пользователю через watchlist @ОБД
        #pair = (TradingPair
        #        .select()
        #        .join(WatchList)
        #        .where(
        #    (TradingPair.pair_id == pair_id) &
        #    (WatchList.user == user_id)
        #)
        #        .get())

        #symbol = pair.symbol
        #pair.delete_instance()

        symbol = get_pair_symbol(pair_id, user_id)  # получаем символ (тикер) торговой пары
        if symbol is None:
            symbol = "не получили символ"
        print('Получили символ торговой пары:', symbol)

        #bot.answer_callback_query(
        #    call.id,
        #    f"Пара {symbol} удалена из списка!"
        #)
        if delete_trading_pair(pair_id, user_id):
            # print('Удалили торговую пару') # Отладка
            bot.answer_callback_query(call.id, f"Пара {symbol} удалена")
        else:
            bot.answer_callback_query(call.id, "Ошибка при удалении пары")

    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Ошибка в формате данных кнопки")
    except Exception as e:
        # print(f"Ошибка при удалении пары!!!!!!!: {str(e)}")  # Отладка
        bot.answer_callback_query(call.id, "Ошибка при удалении пары!")

    finally:
        # Возвращаемся к просмотру списка
        new_call = call
        new_call.data = f"show_list:{list_id}"
        callback_query_handlers.handle_list_selection(new_call)

