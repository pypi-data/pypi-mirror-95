#!/usr/bin/env python3
"""
Пример текстового процессора для Astresay. Аргументом для него
выступает текст, полученный в процессе работы диалога.

Тестирование:

    ./are_you_from.py "я живу в комсомольске на амуре"
    ./are_you_from.py "комсомольск-на-амуре"

"""

import sys

try:
    # Предпочтительнее использовать эту библиотеку, она на C.
    from Levenshtein import distance
except ImportError:
    from astersay.utils import levenshtein_distance as distance


# Варианты названий населённых пунктов, их минимальныая дистанция нахождения
# и настоящее название, возвращаемое в диалог.
NAMES = {
    'москва': (3, 'Москва'),
    'санкт': (3, 'Санкт-Петербург'),
    'санкт петербург': (3, 'Санкт-Петербург'),
    'петербург': (3, 'Санкт-Петербург'),
    'питер': (2, 'Санкт-Петербург'),
    'ленинград': (3, 'Санкт-Петербург'),
    'новосибирск': (3, 'Новосибирск'),
    'екатеринбург': (4, 'Екатеринбург'),
    'екатерин': (3, 'Екатеринбург'),
    'омск': (1, 'Омск'),
    'томск': (1, 'Томск'),
    'тула': (1, 'Тула'),
    'ярославль': (3, 'Ярославль'),
    'ростов на дону': (4, 'Ростов-на-Дону'),
    'ростов': (3, 'Ростов'),
    'ростов': (3, 'Ростов'),
    'артём': (3, 'Артём'),
    'артем': (3, 'Артём'),
    'владивосток': (3, 'Владивосток'),
    'хабаровск': (3, 'Хабаровск'),
    'комсомольск на амуре': (5, 'Комсомольск-на-Амуре'),
    'комсомольск': (3, 'Комсомольск-на-Амуре'),
    'биробиджан': (3, 'Биробиджан'),
    'амгунь': (3, 'Амгунь'),
    'чугуевка': (3, 'посёлок Чугуевка'),
    'чугуев': (3, 'посёлок Чугуевка'),
}


def send_result(key):
    """
    Выводим на стандартный вывод текст, чтобы передать его обратно в диалог.
    """
    if key in NAMES:
        value = NAMES[key][1]
    else:
        value = ''
    print(value)
    return value


def get_text_index(text):
    """Возвращает минимальный индекс дистанции по всему тексту."""
    index = []
    for key, value in NAMES.items():
        d = distance(text, key)
        if value[0] >= d:
            index.append((d, key))
    index.sort()
    return index[0] if index else None


def get_word_index(text):
    """Возвращает минимальный индекс дистанции по словам."""
    words = [x for x in text.split(' ') if x]
    index = []
    for key, value in NAMES.items():
        minimum = value[0]
        for word in words:
            d = distance(word, key)
            if minimum >= d:
                index.append((d, key))
    index.sort()
    return index[0] if index else None


def process(text):
    """
    Производит всю необходимую обработку текста и отправляет найденное
    в диалог.
    """
    text_index = get_text_index(text)
    # Когда текст полностью подходит с нулевой дистанцией.
    if text_index and text_index[0] == 0:
        return send_result(text_index[1])

    word_index = get_word_index(text)
    # Когда слово полностью подходит с нулевой дистанцией.
    if word_index and word_index[0] == 0:
        return send_result(word_index[1])

    # Выбираем наименьшее.
    if text_index and word_index:
        if text_index[0] <= word_index[0]:
            return send_result(text_index[1])
        return send_result(word_index[1])
    elif text_index:
        return send_result(text_index[1])
    elif word_index:
        return send_result(word_index[1])

    return send_result('')


# Текст из буфера диалога приходит одним параметром, слова разделены пробелами.
process(sys.argv[1].lower())
# Обязательно указываем, что плагин успешно завершён, чтобы не прервать диалог.
sys.exit()
