# Функция возвращает построчную информацию о торговых парах:
# символ роста или падения, тикер, цену, изменение цены за последние 24 часа
from binance_api import BinanceAPI
from config import THRESHOLD_OF_LIST_LENGTH_FOR_QUERY_MODE
from typing import List
from other_functions.trace_function_call import trace_function_call


# Функция возвращает построчную информацию о торговых парах:
# символ роста или падения, тикер, цену, изменение цены за последние 24 часа
def get_pairs_info(pairs: List, pair_is_object=True) -> str:
    """
    Возвращение в текстовом виде информации о запрошенных торговых парах:
    В каждой строке: символ роста или падения, тикер, цена, изменение цены за последние 24 часа
    """
    trace_function_call()
    # print("Запущена функция get_pairs_info")
    if len(pairs) == 0:
        pairs_text = "Список пока пуст."
    # если в списке пороговое количество пар или менее, будем получать информацию, запрашивая ее по очереди
    # для каждой пары (сколько пар в списке - столько запросов)
    elif len(pairs) <= THRESHOLD_OF_LIST_LENGTH_FOR_QUERY_MODE:
        # Получаем пары из списка и их текущие цены
        pairs_text = ""
        for pair in pairs:
            symbol = pair.symbol if pair_is_object else pair
            try:
                # Получаем форматированную цену и изменение
                r_o_f, price_info = BinanceAPI.format_price_change(symbol)
                pairs_text += f"{r_o_f} {symbol}: {price_info}\n"
            except:
                pairs_text += f"{symbol}: Ошибка получения данных\n"
    # если в списке более порогового количество пар, делаем запрос без параметра, и отбираем из массива
    # полученной информации только нужные нам пары:
    else:
        # получаем список тикетов ("символов") пар:
        list_of_pairs = []
        for pair in pairs:
            symbol = pair.symbol if pair_is_object else pair
            list_of_pairs.append(symbol)  # добавляем очередной тикет ("символ")

        #  Получаем форматированный текст с символами изменения, тикерами пар, ценой и величиной изменения:
        pairs_text = ''
        try:
            pairs_text = BinanceAPI.get_pairs_with_prices_as_text(list_of_pairs)
        except:
            pairs_text += f"Ошибка получения данных для списка пар: {list_of_pairs}\n"

    return pairs_text

