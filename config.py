import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Настройки базы данных
DB_PATH = "database.db"

# Базовые команды бота
DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Получить справку'),
    ('price', 'Узнать цену пары'),
    ('lists', 'Показать мои списки пар'),
    ('newlist', 'Создать новый список'),
    ('top_gainers', 'Топ-10 растущих пар'),
    ('top_losers', 'Топ-10 падающих пар'),
)


# Настройки API Binance
BINANCE_API_URL = "https://api.binance.com/api/v3"

# Цветовые метки роста и падения цены:
RISING = "🟢"  # (U+1F7E2)
FALLING = "🔴"  # (U+1F534)
UNCHANGED = "⚫"  # (U+26AB)

# Callback-идентификаторы
"""
Идентификаторы callback-команд для инлайн-кнопок.
Используются в callback_data при создании кнопок и в обработчиках callback-запросов.
"""
ADD_PAIR_TO_LIST_PREFIX = "add_pair"  # префикс для добавления торговой пары в список
REMOVE_PAIR_FROM_LIST_PREFIX = "remove_pair"  # префикс для удаления торговой пары из списка
RENAME_LIST_PREFIX = "rename_list"  # префикс для переименования списка торговых пар
DELETE_LIST_PREFIX = "delete_list"  # префикс для удаления списка торговых пар
REMOVE_STARTUP_PREFIX = "remove_startup"  # префикс для отмены показа списка при запуске бота (при выполнении /start)
ADD_STARTUP_PREFIX = "add_startup"  # префикс для установления показа списка при запуске бота (при выполнении /start)
SHOW_LIST_PREFIX = "show_list"  # префикс для показа списка торговых пар с кнопками управления
CANCEL_DELETE_LIST_PREFIX = "cancel_delete"  # префикс для отмены удаления списка
CANCEL_SHOW_PAIRS = 'cancel_pairs'  # callback-команда отмены показа найденных торговых пар
CONFIRM_DELETE_LIST_PREFIX = 'confirm_delete'  # префикс для подтверждения удаления списка
DELETE_THE_PAIR_PREFIX = 'delete_pair'  # префикс для удаления данной пары из списка
LIST_COMPLETE = 'list_complete'  # callback-команда завершения редактирования списка
REMOVE_SOME_PAIR_BUTTON_PREFIX = 'remove_pair'  # префикс кнопки "Удалить пару" (префикс для вывода кнопок
# с тикерами торговых пар для выбора конкретной пары для удаления)
SHOW_PAIRS = 'show_pairs'  # префикс для подтверждения показа всех найденных торговых пар
# (обработчик кнопки "ДА" после вопроса "Найдено N торговых пар. Вы хотите посмотреть все?")

