# Обработчик ввода торговой пары при добавлении в список

from telebot.types import Message
from binance_api import BinanceAPI
from bot_instance import bot, BotStates
from db_operations import get_watchlist, check_pair_exists, create_trading_pair
from keyboards import get_add_more_pair_keyboard
from other_functions.trace_function_call import trace_function_call


# Обработчик ввода торговой пары при добавлении в список
@bot.message_handler(state=BotStates.adding_pair)
def process_add_pair(message: Message):
    """Обработчик ввода торговой пары при добавлении в список"""
    trace_function_call()
    user_id = message.from_user.id
    symbol = message.text.strip().upper()

    # Получаем ID списка из данных состояния
    with bot.retrieve_data(user_id) as data:
        list_id = data['list_id']

    # Проверяем существование пары на Binance
    exists, price = BinanceAPI.check_pair(symbol)
    if not exists:
        bot.send_message(
            user_id,
            f"Ошибка: пара {symbol} не найдена на бирже. "
            "Проверьте правильность написания."
        )
        return

    try:
        watchlist = get_watchlist(list_id, user_id)  # @БД
        if check_pair_exists(watchlist, symbol):
            bot.send_message(user_id, f"Пара {symbol} уже есть в этом списке!")
        else:
            create_trading_pair(watchlist, symbol)
            markup = get_add_more_pair_keyboard(list_id)  # @IK

            # Если цена нулевая, у нас есть дополнение к сообщению
            if price == 0:
                msg_about_zero_price = ("\n\nНулевая цена говорит о том, что пара в настоящее время "
                                        "не торгуется на бирже.")
            else:
                msg_about_zero_price = ""

            # Отправляем основное сообщение
            bot.send_message(
                user_id,
                f'Пара {symbol} успешно добавлена в список "{watchlist.name}"!{msg_about_zero_price}',
                reply_markup=markup
            )

    except Exception as e:
        print(f"Произошла ошибка при добавлении пары. Не удалось подключиться к базе данных: {str(e)}")  # Отладка
        bot.send_message(
            user_id,
            f"Ошибка при добавлении пары. Не удалось подключиться к базе данных. {str(e)}"
        )
