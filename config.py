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

