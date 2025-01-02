# Обработчик команды просмотра списков /lists

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from models import User
from other_functions import rus_number_agreement
from bot_instance import bot
from db_operations import get_user_by_id, get_user_watchlists, get_pairs_count


# Обработчик команды просмотра списков /lists
@bot.message_handler(commands=['lists'])
def handle_show_lists(message: Message):
    """Обработчик команды просмотра списков /lists"""
    user_id = message.from_user.id
    # @ОБД
    #user = User.get_or_none(User.user_id == user_id)
    user = get_user_by_id(user_id)

    if not user:
        bot.reply_to(message, "Сначала нужно выполнить команду /start")
        return

    # Получаем все списки пользователя @ОБД
    #watchlists = user.watchlists
    watchlists = get_user_watchlists(user)

    if not watchlists:
        bot.send_message(
            user_id,
            "У вас пока нет списков.\n"
            "Используйте /newlist чтобы создать новый список."
        )
        return

    # Создаем клавиатуру со списками
    markup = InlineKeyboardMarkup()
    for wlist in watchlists:
        # Получаем количество пар в списке @ОБД
        #pairs_count = wlist.pairs.count()
        pairs_count = get_pairs_count(wlist)
        # Добавляем значок глаза для списка, показываемого при запуске
        eye_icon = " 👁" if wlist.show_on_startup else ""
        markup.add(InlineKeyboardButton(
            f"{wlist.name}{eye_icon} ({rus_number_agreement('', pairs_count, 'пара')})",
            callback_data=f"show_list:{wlist.list_id}"
        ))

    bot.send_message(
        user_id,
        "Ваши списки:\n"
        "Нажмите на список для просмотра пар и управления\n"
        "Символ 👁 означает, что список выводится при запуске бота",
        reply_markup=markup
    )

