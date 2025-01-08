# Обработчик команд получения лидеров роста/падения

from telebot.types import Message
from config import RISING, FALLING, UNCHANGED
from config import NUMBER_OF_MOVERS
from binance_api import BinanceAPI
from bot_instance import bot
from other_functions.trace_function_call import trace_function_call


# Обработчик команд получения лидеров роста/падения
@bot.message_handler(commands=['top_gainers', 'top_losers'])
def handle_top_movers(message: Message):
    """Обработчик команд получения лидеров роста/падения"""
    trace_function_call()
    # Определяем тип запроса по команде
    is_gainers = message.text == '/top_gainers'
    try:
        # Получаем топ растущих/падающих пар (ascending=False для растущих, True для падающих)
        gainers = BinanceAPI.get_top_movers(limit=NUMBER_OF_MOVERS, ascending=not is_gainers)

        response = f"📈 Топ-{NUMBER_OF_MOVERS} {'растущих' if is_gainers else "падающих"} пар:\n\n"
        for pair in gainers:
            symbol = pair['symbol']
            price = float(pair['lastPrice'])
            change = round(float(pair['priceChangePercent']), 1)
            if change == 0:
                change = 0.0  # Если -0.1 < change < 0, то change будет отображаться как -0.0. Убираем это

            # Форматируем цену в зависимости от её величины
            price_fmt = BinanceAPI.format_price(price)

            # Форматируем изменение цены с цветовыми метками
            sign = ''
            if change > 0:
                sign = '+'

            r_o_f = RISING if change > 0 else FALLING if change < 0 else UNCHANGED

            response += f"{r_o_f} {symbol}: {price_fmt} ({sign}{change:.1f}%)\n"

        bot.reply_to(message, response)

    except Exception as e:
        bot.reply_to(
            message,
            f"Ошибка при получении данных о {'растущих' if is_gainers else "падающих"} парах."
        )

