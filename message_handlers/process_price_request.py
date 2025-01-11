# Обработчик запроса цены конкретной пары

from telebot.types import Message
from binance_api import BinanceAPI
from other_functions import rus_number_agreement, show_pairs_info, is_valid_ticker_request
from bot_instance import bot, BotStates
from keyboards import get_show_many_pairs_confirmation_keyboard
from other_functions.trace_function_call import trace_function_call
from config import AUTO_DISPLAY_PAIRS_LIMIT


# Обработчик запроса цены конкретной пары
@bot.message_handler(state=BotStates.waiting_for_symbol)
def process_price_request(message: Message):
    """Обработчик запроса цены конкретной пары"""
    trace_function_call()
    user_id = message.from_user.id
    symbol = message.text.strip().upper()
    matched_pairs = []  # Инициализируем переменную

    # Проверяем запрос на валидность
    if not is_valid_ticker_request(symbol):
        bot.reply_to(message, "Некорректный запрос. Запрос может включать в себя латинские буквы в любом регистре, "
                              "цифры, символы дефиса, подчеркивания, точки, а также символы подстановки * и ?. "
                              "Длина запроса ограничена 20 символами. Попробуйте еще раз.")
        return

    try:
        # Если в запросе есть wildcards
        if '*' in symbol or '?' in symbol:
            matched_pairs = BinanceAPI.find_pairs_by_pattern(symbol)  # @API req

            if not matched_pairs:
                bot.send_message(
                    user_id,
                    "По вашему запросу не найдено торговых пар."
                )
                bot.delete_state(user_id)
                return

            with bot.retrieve_data(user_id) as data:
                data['matched_pairs'] = matched_pairs

            if len(matched_pairs) > AUTO_DISPLAY_PAIRS_LIMIT:  # Если пар найдено больше порогового
                # значения, сообщаем об этом пользователю и запрашиваем подтверждение
                markup = get_show_many_pairs_confirmation_keyboard(symbol)  # @IK

                bot.send_message(
                    user_id,
                    f"{rus_number_agreement('Найдено', len(matched_pairs), 'торговая пара')}. "
                    f"Показать их все?",
                    reply_markup=markup
                )
            else:
                # print("Showing pairs info directly")  # Отладка
                show_pairs_info(user_id, matched_pairs)
                bot.delete_state(user_id)  # Удаляем состояние после показа пар

        else:  # Если это конкретная пара без wildcards
            r_o_f, price_info = BinanceAPI.format_price_change(symbol)
            bot.send_message(
                user_id,
                f"{r_o_f} {symbol}: {price_info}",
            )
            if price_info == '0.00000000':  # Проверка на нулевую цену
                bot.send_message(
                    user_id,
                    f"Нулевая цена говорит о том, что пара в настоящее время не торгуется на Binance."
                )
            bot.delete_state(user_id)  # Удаляем состояние для конкретной пары

    except Exception as e:
        if '*' in symbol or '?' in symbol:
            if matched_pairs:
                bot.send_message(
                    user_id,
                    "Найдены пары, но произошла ошибка при получении цен. "
                    "Пожалуйста, попробуйте позже."
                )
                print(f'Ошибка получения данных о ценах по API: {str(e)}')
            else:
                bot.send_message(
                    user_id,
                    "Произошла ошибка при обработке запроса."
                )
                print(f'Ошибка получения данных по API: {str(e)}')
        else:
            bot.send_message(
                user_id,
                f"Ошибка: не удалось получить цену для пары {symbol}. "
                "Проверьте правильность написания."
            )
        bot.delete_state(user_id)  # Удаляем состояние в случае ошибки

