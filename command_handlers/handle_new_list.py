# Обработчик команды создания нового списка /newlist
from telebot.types import Message
from bot_instance import BotStates
from bot_instance import bot
from db_operations import get_user_by_id
from other_functions.trace_function_call import trace_function_call


# Обработчик команды создания нового списка /newlist
@bot.message_handler(commands=['newlist'])
def handle_new_list(message: Message):
    """Обработчик команды создания нового списка /newlist"""
    trace_function_call()
    user_id = message.from_user.id

    # Проверяем, зарегистрирован ли пользователь
    try:
        if not get_user_by_id(user_id):  # @ОБД
            bot.reply_to(message, "Сначала нужно выполнить команду /start")
            return

        bot.send_message(user_id, "Введите название для нового списка:")
        # Устанавливаем состояние создания списка
        bot.set_state(user_id, BotStates.creating_list)

    except Exception as e:
        print(f'Ошибка соединения с базой данных: {str(e)}')
        bot.reply_to(message, "Не удалось подключиться к базе данных")

