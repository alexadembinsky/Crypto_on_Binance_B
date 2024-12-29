# Обработчик команды получения лидеров роста

from telebot.types import Message
from config import RISING
from binance_api import BinanceAPI
from bot_instance import bot


# Обработчик команды получения лидеров роста
@bot.message_handler(commands=['top_gainers'])
def handle_top_gainers(message: Message):
    """Обработчик команды получения лидеров роста"""
    try:
        # Получаем топ-10 растущих пар
        gainers = BinanceAPI.get_top_movers(limit=10, ascending=False)

        response = "📈 Топ-10 растущих пар:\n\n"
        for pair in gainers:
            symbol = pair['symbol']
            price = float(pair['lastPrice'])
            change = float(pair['priceChangePercent'])

            # Форматируем цену в зависимости от её величины
            if price < 0.01:
                price_fmt = f"{price:.8f}"
            elif price < 1:
                price_fmt = f"{price:.6f}"
            elif price < 100:
                price_fmt = f"{price:.4f}"
            else:
                price_fmt = f"{price:.2f}"

            response += f"{RISING} {symbol}: {price_fmt} (+{change:.1f}%)\n"

        bot.reply_to(message, response)

    except Exception as e:
        bot.reply_to(
            message,
            "Ошибка при получении данных о растущих парах."
        )

