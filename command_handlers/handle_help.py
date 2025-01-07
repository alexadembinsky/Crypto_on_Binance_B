# Обработчик команды /help
from bot_instance import bot
from config import DEFAULT_COMMANDS, HELP_TEXT
from other_functions.trace_function_call import trace_function_call


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    """Обработчик команды /help"""
    trace_function_call()
    help_with_commands_description = HELP_TEXT  # Добавляем в вывод текста справки собственно текст без описаний команд
    for command, description in DEFAULT_COMMANDS:  # Добавляем в вывод текста справки описания каждой команды:
        help_with_commands_description = f"{help_with_commands_description}/{command} - {description}\n"

    bot.reply_to(message, help_with_commands_description)
