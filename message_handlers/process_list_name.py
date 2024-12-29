# Обработчик ввода названия списка

from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from models import User, WatchList
from peewee import IntegrityError

from bot_instance import bot
from bot_instance import BotStates


# Обработчик ввода названия списка
@bot.message_handler(state=BotStates.creating_list)
def process_list_name(message: Message):
    """Обработчик ввода названия списка"""
    user_id = message.from_user.id
    list_name = message.text.strip()

    # Проверяем длину названия
    if len(list_name) < 1 or len(list_name) > 50:
        bot.send_message(user_id, "Название должно быть от 1 до 50 символов. Попробуйте ещё раз:")
        return

    try:
        # Создаем новый список
        user = User.get(User.user_id == user_id)
        watchlist = WatchList.create(
            user=user,
            name=list_name
        )

        # Создаем клавиатуру с кнопками
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Добавить пару", callback_data=f"add_pair:{watchlist.list_id}"),
            InlineKeyboardButton("Переименовать", callback_data=f"rename_list:{watchlist.list_id}"),
            InlineKeyboardButton("Удалить список", callback_data=f"delete_list:{watchlist.list_id}")
        )

        # Отправляем сообщение с кнопками
        bot.send_message(
            user_id,
            f"Список '{list_name}' успешно создан!",
            reply_markup=markup
        )

        # Сбрасываем состояние
        bot.delete_state(user_id)

    except IntegrityError:
        bot.send_message(
            user_id,
            f"У вас уже есть список с названием '{list_name}'. Введите другое название:")

