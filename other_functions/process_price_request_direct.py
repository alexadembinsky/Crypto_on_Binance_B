# обработка запроса цены (без установки состояния) при вводе в строку сообщения

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from binance_api import BinanceAPI
from other_functions import rus_number_agreement, show_pairs_info
from bot_instance import bot, BotStates
from other_functions.trace_function_call import trace_function_call


# обработка запроса цены (без установки состояния) при вводе в строку сообщения
def process_price_request_direct(message: Message, symbol: str):
    """
    Прямая обработка запроса цены (без установки состояния) при вводе в строку сообщения
    Копирует логику из process_price_request, но без работы с состояниями
    """
    trace_function_call()
    user_id = message.from_user.id
    matched_pairs = []

    try:
        # Если в запросе есть wildcards
        if '*' in symbol or '?' in symbol:
            matched_pairs = BinanceAPI.find_pairs_by_pattern(symbol)

            if not matched_pairs:
                bot.send_message(
                    user_id,
                    "По вашему запросу не найдено торговых пар."
                )
                return

            if len(matched_pairs) > 20:
                # Устанавливаем состояние перед сохранением данных
                bot.set_state(user_id, BotStates.waiting_for_symbol)
                with bot.retrieve_data(user_id) as data:
                    data['matched_pairs'] = matched_pairs

                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton("ДА", callback_data=f"show_pairs:{symbol}"),
                    InlineKeyboardButton("НЕТ", callback_data="cancel_pairs")
                )

                bot.send_message(
                    user_id,
                    f"{rus_number_agreement('Найдено', len(matched_pairs), "торговая пара")}. Показать их все?",
                    reply_markup=markup
                )

            else:
                show_pairs_info(user_id, matched_pairs)

        else:  # Если это конкретная пара без wildcards
            r_o_f, price_info = BinanceAPI.format_price_change(symbol)
            bot.send_message(
                user_id,
                f"{r_o_f} {symbol}: {price_info}",
            )
            if price_info == '0.00000000':  # Проверка на нулевую цену
                bot.send_message(
                    user_id,
                    f"Нулевая цена говорит о том, что пара в настоящее время не торгуется на Binance"
                )

    except Exception as e:
        if '*' in symbol or '?' in symbol:
            if matched_pairs:
                bot.send_message(
                    user_id,
                    "Найдены пары, но произошла ошибка при получении цен. "
                    "Пожалуйста, попробуйте позже."
                )
            else:
                bot.send_message(
                    user_id,
                    "Произошла ошибка при обработке запроса."
                )
        else:
            bot.send_message(
                user_id,
                f"Ошибка: не удалось получить цену для пары {symbol}. "
                "Проверьте правильность написания."
            )

