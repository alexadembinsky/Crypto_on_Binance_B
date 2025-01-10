# Операции с базой данных

# Перечень нижеследующих функций:
# About user:
# get_user_by_id - Получить пользователя по ID
# create_user - Создать нового пользователя
# get_user_watchlists - Получить все списки пользователя
#
# About watchlist:
# get_watchlist - Получить список по ID и ID пользователя
# get_watchlist_name - Получить название списка по ID и ID пользователя
# create_watchlist - Создать новый список
# get_watchlist_pairs - Получить все пары из списка
# set_startup_list - Установить список для показа при запуске

# delete_watchlist - Удалить список
# rename_watchlist - Переименовать список
# get_startup_list - Получить список для показа при запуске
# check_list_exists - Проверить существование списка с таким именем у пользователя
# create_list_with_validation - Создать новый список с проверками
# get_pairs_count - Получить количество пар в списке
# disable_startup_list - Отключить показ списка при запуске

# About trading pair:
# get_trading_pair - Получить торговую пару по ID с проверкой принадлежности пользователю
# create_trading_pair - Создать новую торговую пару
# check_pair_exists - Проверить существование пары в списке
# delete_trading_pair - Удалить торговую пару
# get_pair_symbol - Получить символ (тикер) торговой пары по её ID

from typing import Optional, List, Tuple
from models import User, WatchList, TradingPair
from peewee import Model
from peewee import DoesNotExist, IntegrityError, DatabaseError
from other_functions.trace_function_call import trace_function_call


def get_user_by_id(user_id: int) -> Optional[User]:
    """Получить пользователя по ID"""
    trace_function_call()
    return User.get_or_none(User.user_id == user_id)


def create_user(user_id: int, username: str, first_name: str, last_name: str) -> User:
    """Создать нового пользователя"""
    trace_function_call()
    return User.create(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )


def get_user_watchlists(user: User) -> List[WatchList]:
    """Получить все списки пользователя"""
    trace_function_call()
    return list(WatchList.select().where(WatchList.user == user))


def get_watchlist(list_id: int, user_id: int) -> Optional[WatchList]:
    """Получить список по ID и ID пользователя"""
    trace_function_call()
    return WatchList.get_or_none(
        (WatchList.list_id == list_id) &
        (WatchList.user == user_id)
    )


def get_watchlist_name(list_id: int, user_id: int) -> Optional[str]:
    """Получить название списка по ID и ID пользователя"""
    trace_function_call()
    # print('Запущена функция get_watchlist_name()')
    watchlist = WatchList.get_or_none(
        (WatchList.list_id == list_id) &
        (WatchList.user == user_id)
    )
    # print('Функция get_watchlist_name() - строка 38')
    return watchlist.name


def create_watchlist(user: User, name: str, show_on_startup: bool = False) -> WatchList:
    """Создать новый список"""
    trace_function_call()
    return WatchList.create(
        user=user,
        name=name,
        show_on_startup=show_on_startup
    )


def get_watchlist_pairs(watchlist: WatchList) -> List[TradingPair]:
    """Получить все пары из списка"""
    trace_function_call()
    try:
        return list(TradingPair.select().where(TradingPair.watchlist == watchlist))
    except Exception as e:
        print(f'Ошибка получения всех пар из списка "{watchlist.name}": {e}')


def set_startup_list(user_id: int, list_id: int) -> None:
    """Установить список для показа при запуске"""
    trace_function_call()
    WatchList.update(show_on_startup=False).where(
        WatchList.user == user_id
    ).execute()

    watchlist = get_watchlist(list_id, user_id)
    if watchlist:
        watchlist.show_on_startup = True
        watchlist.save()


def disable_startup_list(list_id: int, user_id: int) -> Tuple[bool, None | bool |str]:
    """
    Отключить показ списка при запуске

    Returns:
        Tuple[bool, str]: (успех операции, сообщение об успехе/ошибке)
    """
    trace_function_call()
    try:
        watchlist = get_watchlist(list_id, user_id)
        if not watchlist:
            return True, None

        watchlist.show_on_startup = False
        watchlist.save()
        return True, True

    except Exception as e:
        return False, f"Ошибка при отмене показа списка: {str(e)}"


def delete_watchlist(list_id: int, user_id: int):
    """Удалить список"""
    trace_function_call()
    try:
        watchlist = get_watchlist(list_id, user_id)
        if watchlist:
            watchlist.delete_instance(recursive=True)
    except Exception as e:
        print(f'Ошибка удаления листа (list_id={list_id}, user_id={user_id}): {e}')


def rename_watchlist(watchlist: WatchList, new_name: str):
    """Переименовать список"""
    trace_function_call()
    # watchlist = get_watchlist(list_id, user_id)
    try:
        watchlist.name = new_name
        watchlist.save()
    except Exception as e:
        print(f'Ошибка переименования листа "{watchlist.name}": {e}')


def get_startup_list(user_id: int) -> Optional[WatchList]:
    """Получить список для показа при запуске"""
    trace_function_call()
    return WatchList.get_or_none(
        (WatchList.user == user_id) &
        (WatchList.show_on_startup == True)
    )


def check_list_exists(user_id: int, list_name: str) -> bool:
    """Проверить существование списка с таким именем у пользователя"""
    trace_function_call()
    return WatchList.select().join(User).where(
        (User.user_id == user_id) &
        (WatchList.name == list_name)
    ).exists()


def get_trading_pair(pair_id: int, user_id: int) -> Optional[TradingPair]:
    """Получить торговую пару по ID с проверкой принадлежности пользователю"""
    trace_function_call()
    try:
        return (TradingPair
                .select()
                .join(WatchList)
                .where(
            (TradingPair.pair_id == pair_id) &
            (WatchList.user == user_id)
        )
                .get())
    except DoesNotExist:
        return None


def create_trading_pair(watchlist: WatchList, symbol: str) -> TradingPair:
    """Создать новую торговую пару"""
    trace_function_call()
    return TradingPair.create(
        watchlist=watchlist,
        symbol=symbol
    )


def check_pair_exists(watchlist: WatchList, symbol: str) -> bool:
    """Проверить существование пары в списке"""
    trace_function_call()
    return TradingPair.get_or_none(
        (TradingPair.watchlist == watchlist) &
        (TradingPair.symbol == symbol)
    ) is not None


def create_list_with_validation(user_id: int, list_name: str) -> Tuple[Optional[WatchList], Optional[str]]:
    """
    Создать новый список с проверками

    Returns:
        Tuple[WatchList|None, str|None]: (созданный список, сообщение об ошибке)
    """
    trace_function_call()
    try:
        user = get_user_by_id(user_id)
        if not user:
            return None, "Пользователь не найден"

        if check_list_exists(user_id, list_name):
            return None, f"У вас уже есть список с названием '{list_name}'"

        watchlist = create_watchlist(user, list_name)
        return watchlist, None

    except DatabaseError as e:
        return None, f"Ошибка базы данных: {str(e)}"
    except Exception as e:
        return None, f"Непредвиденная ошибка: {str(e)}"


def get_pairs_count(watchlist: WatchList) -> int:
    """Получить количество пар в списке"""
    trace_function_call()
    return TradingPair.select().where(TradingPair.watchlist == watchlist).count()


def delete_trading_pair(pair_id: int, user_id: int) -> bool:
    """
    Удалить торговую пару

    Returns:
        bool: True если пара успешно удалена, False если пара не найдена
    """
    trace_function_call()
    try:
        pair = (TradingPair
                .select()
                .join(WatchList)
                .where(
            (TradingPair.pair_id == pair_id) &
            (WatchList.user == user_id)
        )
                .get())
        pair.delete_instance()
        return True
    except DoesNotExist:
        return False


def get_pair_symbol(pair_id: int, user_id: int) -> Optional[str]:
    """
    Получить символ (тикер) торговой пары по её ID

    Args:
        pair_id: ID торговой пары
        user_id: ID пользователя (для проверки прав доступа)

    Returns:
        Символ пары или None, если пара не найдена или не принадлежит пользователю
    """
    trace_function_call()
    pair = (TradingPair
            .select()
            .join(WatchList)
            .where(
        (TradingPair.pair_id == pair_id) &
        (WatchList.user == user_id)
    )
            .first())

    return pair.symbol if pair else None
