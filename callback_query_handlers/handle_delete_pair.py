# обработчик выбора пары для удаления из списка
# (обработчик кнопки с тикером торговой пары, нажатие на которую приводит к удалению торговой пары из списка)

from telebot.types import CallbackQuery
from bot_instance import bot
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
        print('Ошибка формата данных при выборе пары для удаления')  # error message
        bot.answer_callback_query(call.id, "Ошибка формата данных")
        return

    list_id = int(parts[1])
    pair_id = int(parts[2])
    symbol = ''

    try:
        symbol = get_pair_symbol(pair_id, user_id)  # получаем символ (тикер) торговой пары @ОБД
        if symbol is None:
            symbol = ''
    except Exception as e:
        print(f"Ошибка при получении символа (тикера) торговой пары: {str(e)}")  # error message

    try:
        delete_trading_pair(pair_id, user_id)  # удаляем торговую пару @ОБД
        bot.answer_callback_query(call.id, f"Пара {symbol}{' ' if symbol else ''}удалена")
    except (ValueError, IndexError) as e:
        bot.answer_callback_query(call.id, "Торговую пару удалить не удалось")
        print(f"Ошибка в формате данных кнопки при попытке удаления торговой пары из списка: {str(e)}")  # error message
    except Exception as e:
        bot.answer_callback_query(call.id, "Ошибка при удалении пары из списка.")
        print(f"Ошибка при попытке удаления торговой пары из списка: {str(e)}")  # error message
    finally:
        # Возвращаемся к просмотру списка
        new_call = call
        new_call.data = f"show_list:{list_id}"
        callback_query_handlers.handle_list_selection(new_call)

