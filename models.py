from datetime import datetime
from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    IntegerField,
    DateTimeField,
    ForeignKeyField,
    AutoField,
    BooleanField
)
from config import DB_PATH

# Инициализация базы данных
db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    """Базовая модель с общими настройками"""
    class Meta:
        database = db


class User(BaseModel):
    """Модель пользователя бота"""
    user_id = IntegerField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField()
    last_name = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)


class WatchList(BaseModel):
    """Модель списка отслеживаемых пар"""
    list_id = AutoField()
    user = ForeignKeyField(User, backref='watchlists')
    name = CharField()
    show_on_startup = BooleanField(default=False)  # показывать список при запуске бота
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        # Создаем уникальный индекс для комбинации пользователя и названия списка
        indexes = (
            (('user', 'name'), True),
        )


class TradingPair(BaseModel):
    """Модель торговой пары в списке наблюдения"""
    pair_id = AutoField()
    watchlist = ForeignKeyField(WatchList, backref='pairs')
    symbol = CharField()  # Например: 'BTCUSDT'
    added_at = DateTimeField(default=datetime.now)


def create_tables():
    """Создание всех таблиц в базе данных"""
    with db:
        db.create_tables([User, WatchList, TradingPair])


def init_db():
    """Инициализация базы данных"""
    create_tables()
    print("База данных успешно инициализирована")

