# Обработчик команды /price - Показать цену заданной торговой пары или группы сходных по тикеру пар
# (при использовании запроса с символами подстановки)

from telebot.types import Message
from bot_instance import bot, BotStates


# Обработчик команды /price - Показать цену заданной торговой пары или группы сходных по тикеру пар
# (при использовании запроса с символами подстановки)
@bot.message_handler(commands=['price'])
def handle_price_command(message: Message):
    """
    Обработчик команды /price - Показать цену заданной торговой пары или группы сходных по тикеру пар
    (при использовании запроса с символами подстановки)
    """
    # print('Запущена функция handle_price_command()') # Отладка
    bot.send_message(
        message.chat.id,
        "Введите тикер торговой пары (например, BTCUSDT).\n"
        'Вы можете использовать символы "*" и "?".\n "*" означает любое количество '
        'любых символов, "?" - ровно один любой символ.\n'
        'Например, "BTC*", "BTCUSD?"'
    )
    bot.set_state(message.from_user.id, BotStates.waiting_for_symbol)

