import requests
from typing import Dict, List, Optional, Tuple
import re
from config import BINANCE_API_URL, RISING, FALLING, UNCHANGED
from other_functions.trace_function_call import trace_function_call


class BinanceAPI:
    """Класс для работы с API Binance"""

    @staticmethod
    def get_ticker_24h(symbol: Optional[str] = None) -> Dict:
        """
        Получение данных о торгах за 24 часа
        :param symbol: Торговая пара (например, 'BTCUSDT')
        :return: Словарь с данными
        """
        trace_function_call()
        endpoint = f"{BINANCE_API_URL}/ticker/24hr"
        params = {'symbol': symbol} if symbol else {}

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def format_price(price: float) -> str:
        """Форматирование цены в зависимости от величины"""
        trace_function_call()
        if price < 0.01:
            return f"{price:.8f}"
        elif price < 1:
            return f"{price:.6f}"
        elif price < 100:
            return f"{price:.4f}"
        else:
            return f"{price:.2f}"

    @staticmethod
    def get_pairs_with_prices(pairs: List[str]) -> Dict[str, Dict[str, float]]:
        trace_function_call()

        """
        Получение цен и изменений для списка пар одним запросом без параметров
        :param pairs: Список торговых пар
        :return: Словарь {пара: {'price': цена, 'change': изменение}}
        """
        try:
            data = BinanceAPI.get_ticker_24h()
            result = {}

            for item in data:
                symbol = item['symbol']
                if symbol in pairs:
                    result[symbol] = {
                        'price': float(item['lastPrice']),
                        'change': float(item['priceChangePercent'])
                    }

            return result
        except Exception as e:
            print(f"Функция get_pairs_with_prices: ошибка при получении цен и изменений для списка пар: {str(e)}")
            raise

    @staticmethod
    def get_pairs_with_prices_as_text(pairs: List[str]) -> str:
        trace_function_call()

        """
        Получение цен и изменений для списка пар в виде отформатированного текста с цветовым символом роста/падения
        :param pairs: Список торговых пар
        :return: Словарь {пара: {'price': цена, 'change': изменение}}
        """
        try:
            data = BinanceAPI.get_pairs_with_prices(pairs)  # запрашиваем данные у биржи одним запросом
            result = ""
            for pair in data.keys():
                change = round(data[pair]['change'], 1)
                if change == 0:
                    change = 0.0  # Если -0.1 < change < 0, то change будет отображаться как -0.0. Убираем это

                price_fmt = BinanceAPI.format_price(data[pair]['price'])

                # Форматируем изменение цены с цветовыми метками
                sign = ''
                change_fmt = f'{change:.1f}%'
                if change > 0:
                    sign = '+'

                # Цветовой символ изменения цены за прошедшие 24 часа:
                r_o_f = RISING if change > 0 else FALLING if change < 0 else UNCHANGED

                # Собираем одну строку результата воедино: цветовая метка роста/падения, тикер, цена, изменение
                # за 24 часа с корректным знаком ("+", если изменение >= 0.1%, "-", если <= 0.1%, иначе без знака
                result = f'{result}\n{r_o_f} {pair} {price_fmt} ({sign}{change_fmt})'

            return result
        except Exception as e:
            print(f"Функция get_pairs_with_prices_as_text: ошибка при создании форматированного "
                  f"списка пар с цветовыми символами изменения, тикером, форматированной ценой и форматированным "
                  f"изменением за 24 часа: {str(e)}")
            raise

    @staticmethod
    def format_price_change(symbol: str) -> Tuple[bool, str]:
        """
        Форматирование цены и изменения для пары
        :param symbol: Торговая пара (например, 'BTCUSDT')
        :return: Отформатированная строка с ценой и изменением
        """
        trace_function_call()

        try:
            data = BinanceAPI.get_ticker_24h(symbol)
            price = float(data['lastPrice'])
            change = round(float(data['priceChangePercent']), 1)
            if change == 0:
                change = 0.0  # Если -0.1 < change < 0, то change будет отображаться как -0.0. Убираем это

            price_fmt = BinanceAPI.format_price(price)

            # Форматируем изменение цены с цветовыми метками
            sign = ''
            change_fmt = f'{change:.1f}%'
            if change > 0:
                sign = '+'

            return RISING if change > 0 else FALLING if change < 0 else UNCHANGED, f"{price_fmt} ({sign}{change_fmt})"
        except Exception as e:
            print(f"Не найден тикер по запросу {symbol}: {str(e)}")
            raise

    @staticmethod
    def find_pairs_by_pattern(pattern: str) -> List[str]:
        """
        Поиск торговых пар по шаблону с поддержкой * и ?
        :param pattern: Шаблон поиска (например, 'BTC*', 'BTCUSD?')
        :return: Список найденных пар (исключая пары с нулевой ценой)
        """
        trace_function_call()
        data = BinanceAPI.get_ticker_24h()
        regex_pattern = pattern.replace("*", ".*").replace("?", ".")
        regex = re.compile(f"^{regex_pattern}$")

        # Фильтруем пары: проверяем и шаблон, и цену
        return [
            item['symbol'] for item in data
            if regex.match(item['symbol']) and float(item['lastPrice']) > 0]

    @staticmethod
    def get_top_movers(limit: int = 10, ascending: bool = False) -> List[Dict]:
        """
        Получение списка пар с наибольшим изменением цены
        :param limit: Количество пар в результате
        :param ascending: True для получения падающих пар, False для растущих
        :return: Список словарей с данными
        """
        trace_function_call()
        data = BinanceAPI.get_ticker_24h()
        sorted_data = sorted(
            data,
            key=lambda x: float(x['priceChangePercent']),
            reverse=not ascending
        )
        return sorted_data[:limit]

    @staticmethod
    def check_pair(symbol: str) -> tuple[bool, float]:
        """
        Проверка существования пары и получение её цены
        :param symbol: Торговая пара (например, 'BTCUSDT')
        :return: Кортеж (существует ли пара, цена пары)
        """
        trace_function_call()
        try:
            data = BinanceAPI.get_ticker_24h(symbol)
            price = float(data['lastPrice'])
            return True, price
        except Exception as e:
            print(f"Error checking pair {symbol}: {str(e)}")
            return False, 0.0
