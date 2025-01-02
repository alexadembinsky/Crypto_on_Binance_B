# Обработчик ввода нового названия списка

from telebot.types import Message
from models import WatchList
from peewee import IntegrityError
from bot_instance import bot, BotStates
from db_operations import get_watchlist, rename_watchlist


# Обработчик ввода нового названия списка
@bot.message_handler(state=BotStates.renaming_list)
def process_rename_list(message: Message):
    """Обработчик ввода нового названия списка"""
    user_id = message.from_user.id
    new_name = message.text.strip()

    # Проверяем длину названия
    if len(new_name) < 1 or len(new_name) > 50:
        bot.send_message(
            user_id,
            "Название должно быть от 1 до 50 символов. Попробуйте ещё раз:"
        )
        return

    try:
        # Получаем ID списка из данных состояния
        with bot.retrieve_data(user_id) as data:
            list_id = data['list_id']

        # Получаем и переименовываем список @ОБД
        #watchlist = WatchList.get(
        #    (WatchList.list_id == list_id) &
        #    (WatchList.user == user_id)
        #)
        #old_name = watchlist.name
        #watchlist.name = new_name
        #watchlist.save()
        try:
            watchlist = get_watchlist(list_id, user_id)
            old_name = watchlist.name
            try:
                rename_watchlist(watchlist, new_name)

                bot.send_message(
                    user_id,
                    f"Список '{old_name}' переименован в '{new_name}'!"
                )
            except IntegrityError:
                bot.send_message(
                    user_id,
                    f"У вас уже есть список с названием '{new_name}'. "
                    "Введите другое название:"
                )
            except Exception as e:
                bot.send_message(
                    user_id,
                    f"Произошла ошибка при переименовании списка: {str(e)}"
                )
        except Exception as e:
            bot.send_message(
                user_id,
                f"Не удалось получить параметры списка: {str(e)}"
            )
    except Exception as e:
        bot.send_message(
            user_id,
            f"Не удалось получить ID списка из данных состояния: {str(e)}"
        )

    # Сбрасываем состояние
    bot.delete_state(user_id)

