# Функция для number agreement/pluralization в русском языке. Согласует "окружение" чисел по грамматической форме

def rus_number_agreement(pre_word: str, number: int, post_word: str) -> str:
    """
    Функция для number agreement/pluralization в русском языке. Согласует "окружение" чисел по грамматической форме.
    Например, "Найден 21 предмет", "Найдено 22 предмета", "найдено 25 предметов". Предшествующее и последующее
    слово или словосочетание должны входить в словарь NUMERICAL_CONTEXT в качестве ключа.

    Значением ключа является список из трех грамматических форм слова, используемых при указании
    количества/числа предметов, например, ['метр', 'метра', 'метров'].

    Функция возвращает строку, состоящую из самого числа number в строковой форме, пробела и единицы измерения
    или названия предмета в той грамматической форме, которая нужна с данным числом: '1 камень', '3 камня', '16 камней'

    :param pre_word: предшествующее слово, например, "обнаружено", "поставлено"
    :type pre_word: str
    :param number: количество предметов или величина
    :type number: int
    :param post_word: последующее слово (единица измерения или название предмета) (напр., 'килограмм', 'камень')
    :type post_word: str
    :return: строка, состоящая из числа и правильной формы единицы измерения/названия предмета
    (напр., 'Обнаружен 21 камень', 'Поставлены 22 контейнера')
    :rtype: str
    """
    from numerical_context import NUMERICAL_CONTEXT

    # проверка типа аргументов:
    if not isinstance(pre_word, str):
        raise TypeError("Функция rus_number_agreement(): параметр pre_word должен быть строкой")
    if not isinstance(number, int):
        raise TypeError("Функция rus_number_agreement(): параметр number должен быть целым числом")
    if not isinstance(post_word, str):
        raise TypeError("Функция rus_number_agreement(): параметр post_word должен быть строкой")

    # проверка значения аргумента:
    if pre_word != '' and post_word not in NUMERICAL_CONTEXT:
        raise ValueError(f"Функция num_with_rus_units(): слово или словосочетание '{pre_word}' не найдено"
                         f" в словаре NUMERICAL_CONTEXT")
    if post_word != '' and post_word not in NUMERICAL_CONTEXT:
        raise ValueError(f"Функция num_with_rus_units(): слово или словосочетание '{post_word}' не найдено"
                         f" в словаре NUMERICAL_CONTEXT")

    last_digit = number % 10
    second_digit_from_end = (number // 10) % 10

    pre_number_agreed_form = NUMERICAL_CONTEXT[pre_word][2] if pre_word != '' else ''  # наиб. частая форма, "3-я"
    post_number_agreed_form = NUMERICAL_CONTEXT[post_word][2] if post_word != '' else ''  # наиб. частая форма, "3-я"
    if second_digit_from_end != 1:  # если вторая справа цифра не равна 1
        if last_digit == 1:  # если число оканчивается на 1
            pre_number_agreed_form = NUMERICAL_CONTEXT[pre_word][0] if pre_word != '' else ''  # "1-я" форма
            post_number_agreed_form = NUMERICAL_CONTEXT[post_word][0] if post_word != '' else ''  # "1-я" форма
        elif 2 <= last_digit <= 4:  # если число оканчивается на 2, 3, 4
            pre_number_agreed_form = NUMERICAL_CONTEXT[pre_word][1] if pre_word != '' else ''  # "2-я" форма
            post_number_agreed_form = NUMERICAL_CONTEXT[post_word][1] if post_word != '' else ''  # "2-я" форма

    return f'{pre_number_agreed_form}{'' if pre_word == '' else ' '}{number} {post_number_agreed_form}'
