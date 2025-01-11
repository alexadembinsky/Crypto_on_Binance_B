# вывод информации о торговых парах

from typing import List
from bot_instance import bot
from other_functions.get_pairs_info import get_pairs_info
from other_functions.trace_function_call import trace_function_call


# вывод информации о торговых парах
def show_pairs_info(user_id: int, pairs: List[str]):
    """Вывод информации о торговых парах"""
    trace_function_call()
    try:
        # Отправляем сообщение о запросе к бирже и сохраняем его
        loading_message = bot.send_message(
            user_id,
            "⚡ Минутку... Получаю данные с Binance... ⚡"
        )

        # Формируем ответ
        response = "Найденные пары:\n\n"
        response = f'{response}{get_pairs_info(pairs, False)}'  # получаем форматированную информацию о парах

        # Удаляем сообщение о загрузке
        bot.delete_message(
            chat_id=user_id,
            message_id=loading_message.message_id
        )

        # Отправляем основной ответ
        bot.send_message(user_id, response)

    except Exception as e:
        print(f"Ошибка получения данных по API: {str(e)}")  # сообщение об ошибке
        bot.send_message(
            user_id,
            "Произошла ошибка при получении цен."
        )

