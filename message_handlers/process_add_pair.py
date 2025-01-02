# Обработчик ввода торговой пары при добавлении в список

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from models import WatchList, TradingPair
from binance_api import BinanceAPI
from bot_instance import bot, BotStates
from db_operations import get_watchlist, check_pair_exists, create_trading_pair


# Обработчик ввода торговой пары при добавлении в список
@bot.message_handler(state=BotStates.adding_pair)
def process_add_pair(message: Message):
    """Обработчик ввода торговой пары при добавлении в список"""
    user_id = message.from_user.id
    symbol = message.text.strip().upper()

    # Получаем ID списка из данных состояния
    with bot.retrieve_data(user_id) as data:
        list_id = data['list_id']

    try:
        # Проверяем существование пары на Binance
        # data = BinanceAPI.get_ticker_24h(symbol) # старое
        # price = float(data['lastPrice'])  # если пара не существует, будет исключение # старое
        # новое:
        exists, price = BinanceAPI.check_pair(symbol)
        if not exists:
            bot.send_message(
                user_id,
                f"Ошибка: пара {symbol} не найдена на бирже. "
                "Проверьте правильность написания."
            )
            return  # /новое

        # Получаем список: @ОБД
        #watchlist = WatchList.get(
        #    (WatchList.list_id == list_id) &
        #    (WatchList.user == user_id)
        #)
        watchlist = get_watchlist(list_id, user_id)

        # Проверяем, нет ли уже такой пары в списке и, если нет, до добавляем; если есть, сообщаем об этом @ОБД
        #existing_pair = TradingPair.get_or_none(
        #    (TradingPair.watchlist == watchlist) &
        #    (TradingPair.symbol == symbol)
        #)

        #if existing_pair:
        #    bot.send_message(
        #        user_id,
        #        f"Пара {symbol} уже есть в этом списке!"
        #    )
        #else:
        #    # Добавляем новую пару @ОБД
        #    TradingPair.create(
        #        watchlist=watchlist,
        #        symbol=symbol
        #    )
        if check_pair_exists(watchlist, symbol):
            bot.send_message(user_id, f"Пара {symbol} уже есть в этом списке!")
        else:
            create_trading_pair(watchlist, symbol)
            # Выводим клавиатуру добавления еще одной пары
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("Добавить ещё пару", callback_data=f"add_pair:{list_id}"),
                InlineKeyboardButton("Завершить редактирование списка", callback_data="list_complete")
            )
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
        # print(f"Error in process_add_pair: {str(e)}")  # Отладка
        bot.send_message(
            user_id,
            f"Произошла ошибка при добавлении пары: {str(e)}"
        )

    finally:
        # Сбрасываем состояние
        bot.delete_state(user_id)
