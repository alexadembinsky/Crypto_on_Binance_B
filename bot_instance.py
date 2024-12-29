import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.custom_filters import StateFilter
from config import BOT_TOKEN


# Инициализация бота с хранилищем состояний
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)

# Добавляем фильтр состояний
bot.add_custom_filter(StateFilter(bot))


class BotStates(StatesGroup):
    """Класс для хранения состояний бота"""
    creating_list = State()  # Создание нового списка
    adding_pair = State()  # Добавление пары
    renaming_list = State()  # Переименование списка
    selecting_list = State()  # Выбор списка для действий
    waiting_for_symbol = State()  # Ожидание ввода символа пары
