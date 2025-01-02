# Обработчик команды создания нового списка /newlist
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from models import User
from bot_instance import BotStates
from bot_instance import bot
from db_operations import get_user_by_id


# Обработчик команды создания нового списка /newlist
@bot.message_handler(commands=['newlist'])
def handle_new_list(message: Message):
    """Обработчик команды создания нового списка /newlist"""
    user_id = message.from_user.id

    # Проверяем, зарегистрирован ли пользователь @ОБД
    #if not User.get_or_none(User.user_id == user_id):
    #    bot.reply_to(message, "Сначала нужно выполнить команду /start")
    #    return
    if not get_user_by_id(user_id):
        bot.reply_to(message, "Сначала нужно выполнить команду /start")
        return

    bot.send_message(user_id, "Введите название для нового списка:")
    # Устанавливаем состояние создания списка
    bot.set_state(user_id, BotStates.creating_list)

