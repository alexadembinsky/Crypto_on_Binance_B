# Обработчик команды получения лидеров падения

from telebot.types import Message
from config import FALLING
from binance_api import BinanceAPI
from bot_instance import bot


# Обработчик команды получения лидеров падения
@bot.message_handler(commands=['top_losers'])
def handle_top_losers(message: Message):
    """Обработчик команды получения лидеров падения"""
    try:
        # Получаем топ-10 падающих пар
        losers = BinanceAPI.get_top_movers(limit=10, ascending=True)

        response = "📉 Топ-10 падающих пар:\n\n"
        for pair in losers:
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

            response += f"{FALLING} {symbol}: {price_fmt} ({change:.1f}%)\n"

        bot.reply_to(message, response)

    except Exception as e:
        bot.reply_to(
            message,
            "Ошибка при получении данных о падающих парах."
        )

