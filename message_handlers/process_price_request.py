# Обработчик запроса цены конкретной пары

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from binance_api import BinanceAPI
from other_functions import rus_number_agreement
from bot_instance import bot, BotStates
from other_functions import show_pairs_info
from keyboards import get_show_many_pairs_confirmation_keyboard
from other_functions.trace_function_call import trace_function_call


# Обработчик запроса цены конкретной пары
@bot.message_handler(state=BotStates.waiting_for_symbol)
def process_price_request(message: Message):
    """Обработчик запроса цены конкретной пары"""
    trace_function_call()
    # print('Запущена функция process_price_request - Обработчик запроса цены конкретной пары')  # Отладка
    user_id = message.from_user.id
    symbol = message.text.strip().upper()
    matched_pairs = []  # Инициализируем переменную

    try:
        # Если в запросе есть wildcards
        if '*' in symbol or '?' in symbol:
            # print(f"Processing wildcard pattern: {symbol}")  # Отладка
            matched_pairs = BinanceAPI.find_pairs_by_pattern(symbol)
            print(f"PROCESS PRICE REQUEST 27 Found pairs: {matched_pairs}")  # Отладка

            if not matched_pairs:
                bot.send_message(
                    user_id,
                    "По вашему запросу не найдено торговых пар."
                )
                bot.delete_state(user_id)
                return

            with bot.retrieve_data(user_id) as data:
                data['matched_pairs'] = matched_pairs

            if len(matched_pairs) > 20:
                # Создаем клавиатуру: @IK
                #markup = InlineKeyboardMarkup()
                #markup.add(
                #    InlineKeyboardButton("ДА", callback_data=f"show_pairs:{symbol}"),
                #    InlineKeyboardButton("НЕТ", callback_data="cancel_pairs")
                #)
                markup = get_show_many_pairs_confirmation_keyboard(symbol)

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
        # print(f"Error in process_price_request: {str(e)}")  # Отладка
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
        bot.delete_state(user_id)  # Удаляем состояние в случае ошибки

