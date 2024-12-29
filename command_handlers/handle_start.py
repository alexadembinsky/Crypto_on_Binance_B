# Обработчик команды /start

from models import User, WatchList, TradingPair
from peewee import IntegrityError

from binance_api import BinanceAPI

from bot_instance import bot


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        # Создаем нового пользователя и сохраняем результат в переменную
        new_user = User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        # Создаем базовый список для нового пользователя
        base_list = WatchList.create(
            user=new_user,  # Используем созданного пользователя
            name="Base",
            show_on_startup=True
        )

        # Добавляем базовые пары
        for symbol in ["BTCUSDT", "ETHUSDT"]:
            TradingPair.create(
                watchlist=base_list,
                symbol=symbol
            )

        welcome_text = (
            f"Привет, {first_name}! 👋\n\n"
            "Я бот для отслеживания цены спотовых активов на бирже Binance.\n"
            "Используйте /help для просмотра доступных команд."
        )
    except IntegrityError:
        # Пользователь уже существует
        welcome_text = (
            f"С возвращением, {first_name}! 👋\n"
            "Используйте /help для просмотра доступных команд."
        )

    bot.reply_to(message, welcome_text)

    # Проверяем наличие списка для показа при запуске
    startup_list = WatchList.get_or_none(
        (WatchList.user == user_id) &
        (WatchList.show_on_startup == True)
    )

    if startup_list:
        # Формируем текст со списком пар
        pairs_text = ""
        for pair in startup_list.pairs:
            try:
                r_o_f, price_info = BinanceAPI.format_price_change(pair.symbol)
                pairs_text += f"{r_o_f} {pair.symbol}: {price_info}\n"
            except Exception:
                pairs_text += f"{pair.symbol}: Ошибка получения данных\n"

        if pairs_text:
            bot.send_message(user_id, pairs_text)
