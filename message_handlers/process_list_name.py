# Обработчик ввода названия списка

from telebot.types import Message
from bot_instance import bot
from bot_instance import BotStates
from db_operations import create_list_with_validation
from keyboards import get_new_list_actions_keyboard
from other_functions.trace_function_call import trace_function_call


# Обработчик ввода названия списка
@bot.message_handler(state=BotStates.creating_list)
def process_list_name(message: Message):
    """Обработчик ввода названия списка"""
    trace_function_call()
    user_id = message.from_user.id
    list_name = message.text.strip()

    error = None
    # Проверяем длину названия
    if len(list_name) < 1 or len(list_name) > 50:
        bot.send_message(
            user_id,
            "Название должно быть от 1 до 50 символов. Попробуйте ещё раз:"
        )
        return  # Выходим из функции, состояние сохранится
    try:
        # Создаем список
        watchlist, error = create_list_with_validation(user_id, list_name)  # @ОБД

        if error:  # если произошла ошибка
            if "уже есть список" in error:  # Если список сущ-ет, сообщаем об ошибке и просим ввести другое название
                error += '. Введите другое название:'
            bot.send_message(user_id, error)
            return
        else:  # если список был благополучно создан
            # Создаем клавиатуру с кнопками
            markup = get_new_list_actions_keyboard(watchlist.list_id)  # @IK

            # Отправляем сообщение с кнопками
            bot.send_message(
                user_id,
                f"Список '{list_name}' успешно создан!",
                reply_markup=markup
            )
    except Exception as e:
        print(f'Функция process_list_name(): Произошла непредвиденная ошибка: {e}')
        bot.send_message(
            user_id,
            f"Произошла непредвиденная ошибка: {e}"
        )
    finally:
        if error:  # Если у нас ошибка
            if "уже есть список" in error:  # Если у нас уже есть список с таким названием
                # Оставляем состояние, чтобы пользователь мог повторно ввести название списка, но уже другое
                pass
            else:  # Если ошибка в чем-то другом:
                # Сбрасываем состояние
                bot.delete_state(user_id)
        else:  # Если ошибок нет:
            bot.delete_state(user_id)  # Сбрасываем состояние


