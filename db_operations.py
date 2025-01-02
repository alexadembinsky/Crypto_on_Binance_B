# Операции с базой данных

from typing import Optional, List
from models import User, WatchList, TradingPair
from peewee import Model


def get_user_by_id(user_id: int) -> Optional[User]:
    """Получить пользователя по ID"""
    return User.get_or_none(User.user_id == user_id)


def create_user(user_id: int, username: str, first_name: str, last_name: str) -> User:
    """Создать нового пользователя"""
    return User.create(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )


def get_watchlist(list_id: int, user_id: int) -> Optional[WatchList]:
    """Получить список по ID и ID пользователя"""
    return WatchList.get_or_none(
        (WatchList.list_id == list_id) &
        (WatchList.user == user_id)
    )


def create_watchlist(user: User, name: str, show_on_startup: bool = False) -> WatchList:
    """Создать новый список"""
    return WatchList.create(
        user=user,
        name=name,
        show_on_startup=show_on_startup
    )


def get_user_watchlists(user: User) -> List[WatchList]:
    """Получить все списки пользователя"""
    return list(WatchList.select().where(WatchList.user == user))


def get_watchlist_pairs(watchlist: WatchList) -> List[TradingPair]:
    """Получить все пары из списка"""
    return list(TradingPair.select().where(TradingPair.watchlist == watchlist))


def set_startup_list(user_id: int, list_id: int) -> None:
    """Установить список для показа при запуске"""
    WatchList.update(show_on_startup=False).where(
        WatchList.user == user_id
    ).execute()

    watchlist = get_watchlist(list_id, user_id)
    if watchlist:
        watchlist.show_on_startup = True
        watchlist.save()


def delete_watchlist(list_id: int, user_id: int) -> bool:
    """Удалить список"""
    watchlist = get_watchlist(list_id, user_id)
    if watchlist:
        watchlist.delete_instance(recursive=True)
        return True
    return False


def rename_watchlist(watchlist: WatchList, new_name: str):
    """Переименовать список"""
    # watchlist = get_watchlist(list_id, user_id)
    try:
        watchlist.name = new_name
        watchlist.save()
    except Exception:
        pass


def get_trading_pair(pair_id: int, user_id: int) -> Optional[TradingPair]:
    """Получить торговую пару по ID"""
    return TradingPair.get_or_none(
        (TradingPair.pair_id == pair_id) &
        (TradingPair.watchlist.user == user_id)
    )


def create_trading_pair(watchlist: WatchList, symbol: str) -> TradingPair:
    """Создать новую торговую пару"""
    return TradingPair.create(
        watchlist=watchlist,
        symbol=symbol
    )


def check_pair_exists(watchlist: WatchList, symbol: str) -> bool:
    """Проверить существование пары в списке"""
    return TradingPair.get_or_none(
        (TradingPair.watchlist == watchlist) &
        (TradingPair.symbol == symbol)
    ) is not None


def delete_trading_pair(pair_id: int, user_id: int) -> bool:
    """Удалить торговую пару"""
    pair = get_trading_pair(pair_id, user_id)
    if pair:
        pair.delete_instance()
        return True
    return False


def get_startup_list(user_id: int) -> Optional[WatchList]:
    """Получить список для показа при запуске"""
    return WatchList.get_or_none(
        (WatchList.user == user_id) &
        (WatchList.show_on_startup == True)
    )


def get_pairs_count(watchlist: WatchList) -> int:
    """Получить количество пар в списке"""
    return TradingPair.select().where(TradingPair.watchlist == watchlist).count()

