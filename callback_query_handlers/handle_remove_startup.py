# Обработчик отмены показа списка при запуске

from telebot.types import CallbackQuery
from bot_instance import bot
import callback_query_handlers
from config import REMOVE_STARTUP_PREFIX
from db_operations import disable_startup_list
from other_functions.trace_function_call import trace_function_call


# Обработчик отмены показа списка при запуске
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{REMOVE_STARTUP_PREFIX}:'))
def handle_remove_startup(call: CallbackQuery):
    """Обработчик отмены показа списка при запуске"""
    trace_function_call()
    user_id = call.from_user.id
    list_id = int(call.data.split(':')[1])

    success, message = disable_startup_list(list_id, user_id)  # Отменяем показ списка при запуске @ОБД

    if success:  # Если получен ответ от БД:
        if message:  # Если получен список
            # Выводим сообщение:
            bot.answer_callback_query(
                call.id,
                f'Список не будет выводиться при запуске бота'  # @ОБД
            )
            # Обновляем отображение списка
            new_call = call
            new_call.data = f"show_list:{list_id}"
            callback_query_handlers.handle_list_selection(new_call)

        else:
            print(f'Ошибка: не удалось получить список')
            bot.answer_callback_query(
                call.id,
                f"Ошибка: не удалось получить список."  # @ОБД
            )

    else:
        print(f'Ошибка соединения с базой данных. Не удалось отменить показ списка при запуске: {message}')
        bot.answer_callback_query(
            call.id,
            f"Ошибка соединения с БД. Не удалось отменить показ списка при запуске."  # @ОБД
        )
