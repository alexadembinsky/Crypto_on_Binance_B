# Обработчик команды получения лидеров роста

from telebot.types import Message
from config import RISING
from binance_api import BinanceAPI
from bot_instance import bot
from other_functions.trace_function_call import trace_function_call


# Обработчик команды получения лидеров роста
@bot.message_handler(commands=['top_gainers'])
def handle_top_gainers(message: Message):
    """Обработчик команды получения лидеров роста"""
    trace_function_call()
    try:
        # Получаем топ-10 растущих пар
        gainers = BinanceAPI.get_top_movers(limit=10, ascending=False)

        response = "📈 Топ-10 растущих пар:\n\n"
        for pair in gainers:
            symbol = pair['symbol']
            price = float(pair['lastPrice'])
            change = float(pair['priceChangePercent'])

            # Форматируем цену в зависимости от её величины
            price_fmt = BinanceAPI.format_price(price)

            response += f"{RISING} {symbol}: {price_fmt} (+{change:.1f}%)\n"

        bot.reply_to(message, response)

    except Exception as e:
        bot.reply_to(
            message,
            "Ошибка при получении данных о растущих парах."
        )

