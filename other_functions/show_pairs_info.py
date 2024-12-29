# вывод информации о торговых парах

from binance_api import BinanceAPI
from typing import List
from bot_instance import bot


# вывод информации о торговых парах
def show_pairs_info(user_id: int, pairs: List[str]):
    """Вывод информации о торговых парах"""
    # print('Запущена функция show_pairs_info - Вывод информации о парах', pairs)  # Отладка
    try:
        # print("Getting prices for pairs:", pairs)  # Отладка
        # pairs_prices = BinanceAPI.get_pairs_with_prices(pairs)  # Отладка
        # print("Received prices:", pairs_prices)  # Отладка

        # Отправляем сообщение о запросе к бирже и сохраняем его
        loading_message = bot.send_message(
            user_id,
            "⚡ Минутку... Получаю данные с Binance... ⚡"
        )

        # Формируем ответ
        response = "Найденные пары:\n\n"
        for pair in pairs:
            try:
                r_o_f, price_info = BinanceAPI.format_price_change(pair)
                response += f"{r_o_f} {pair}: {price_info}\n"
            except Exception:
                continue

        # Удаляем сообщение о загрузке
        bot.delete_message(
            chat_id=user_id,
            message_id=loading_message.message_id
        )

        # Отправляем основной ответ
        bot.send_message(user_id, response)

    except Exception as e:
        # print(f"Error in show_pairs_info: {str(e)}")  # Отладка
        bot.send_message(
            user_id,
            "Произошла ошибка при получении цен."
        )

