# Обработчик команды просмотра списков /lists

from telebot.types import Message
from bot_instance import bot
from db_operations import get_user_by_id, get_user_watchlists
from keyboards import get_watchlists_keyboard
from other_functions.trace_function_call import trace_function_call


# Обработчик команды просмотра списков /lists
@bot.message_handler(commands=['lists'])
def handle_show_lists(message: Message):
    """Обработчик команды просмотра списков /lists"""
    trace_function_call()
    user_id = message.from_user.id
    try:
        user = get_user_by_id(user_id)  # @ОБД

        if not user:
            bot.reply_to(message, "Сначала нужно выполнить команду /start")
            return

        # Получаем все списки пользователя @ОБД
        watchlists = get_user_watchlists(user)  # @ОБД

        if not watchlists:
            bot.send_message(
                user_id,
                "У вас пока нет списков.\n"
                "Используйте /newlist чтобы создать новый список."
            )
            return

        # Создаем клавиатуру со списками
        markup = get_watchlists_keyboard(watchlists)  # @IK

        bot.send_message(
            user_id,
            "<b>Ваши списки:</b>\n\n"
            "<i>Нажмите на список для просмотра пар и управления</i>\n"
            "<i>Символ 👁 означает, что список выводится при запуске бота</i>",
            reply_markup=markup,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f'Ошибка соединения с базой данных: {str(e)}')
        bot.reply_to(message, "Не удалось подключиться к базе данных")

