# Skypro. Профессия "Python-разработчик" ПОТОК
# Курс 2
# *******************************
# Урок  6. Локальный Python и фaйлы. Домашнее задание
# Родительский Дмитрий Вячеславович

import os
from random import shuffle, sample
from common import *


def get_question_list():
    """
    Получает список слов из файла со словами,
    обрезает сисмволы перевода строки, получает список
    случайных значений из исходного файла.
    :return: [str, str, ...]
    """
    if os.path.exists(os.path.join(WRK_DIRECTORY, WORDS_FILE)):
        f = open(file=os.path.join(WRK_DIRECTORY, WORDS_FILE), mode="rt", encoding='utf-8')
        try:
            return sample([str(item).strip() for item in f.readlines() if len(str(item).strip()) > 0], TASK_COUNT)
        finally:
            f.close()
    else:
        return []


def get_shuffle_word(src_word: str):
    """
    Перемешивает буквы в принимаемоем слове случайным порядком
    и возврашает слово, которое не должно совпадать с исходным
    :return: str
    """
    shuffle_word = src_word
    while shuffle_word == src_word:
        lst = [letter for letter in src_word]
        shuffle(lst)
        shuffle_word = "".join(lst)
    return shuffle_word


def save_play_history(user_name: str, score: int):
    """
    Сохраняем статистику текущей игры
    (имя пользователя, количество набранных баллов)
    :return:  None
    """
    with open(file=os.path.join(WRK_DIRECTORY, HISTORY_FILE), mode="at", encoding='utf-8') as file:
        file.write(f"{user_name} {score}\n")


def read_user_history(user_name: str):
    """
    Считваем историю статистику игр конкретного пользователся
    Возвращает словарь вида
    :return: { 'total plays' : int,  'best result' : int}
    """
    # Cчетчики игр и максимального количества очков
    max_score = total_play = 0

    # Читаем файл с историей игр в набор строк
    if os.path.exists(os.path.join(WRK_DIRECTORY, HISTORY_FILE)):
        with open(os.path.join(WRK_DIRECTORY, HISTORY_FILE), mode="rt", encoding='utf-8') as file:
            lst = [str(item).strip() for item in file.readlines()]

        # Парсим набор строк и ищем данные по пользователю user_name
        for item in lst:
            # !!! Прием из вебинара !!!!!
            user, score = item.split(" ")

            # Прочитали данные по нашему пользователю -
            # учитываем в его статистике
            if user == user_name:
                total_play += 1
                if int(score) >= max_score:
                    max_score = int(score)

    return {'total plays': total_play, 'best result': max_score}


def main():
    """
    Основная функция приложения - реализует бизнес - логику
    :return: None
    """
    # Считываем из файла список слов для тестирования
    # и перемешиваем его (порядок слов), если не можем загрузить
    # список слов сообщаем пользователю и завершаем программу
    user_tasks_list = get_question_list()
    if len(user_tasks_list) == 0:
        print("Что-то не так со списком заданий")
        print("Пока, пока ....")
        quit()
    print("[+] Начинаем тестирование ...")

    # Ввод имени пользователя (и сделаем первую букву имени заглавной)
    while True:
        user_name = input("Ведите имя пользователя: ").strip().capitalize()
        if user_name != "":
            break

    # счетчик набранных  пользователем баллов баллов
    total = 0
    # Начинаем наш цикл опроса пользователя
    for i, word in enumerate(user_tasks_list, start=1):
        if IS_DEBUG_MSG:
            print(f"Исходное слово >>>> {word} <<<<")

        user_test_word = get_shuffle_word(word)
        while True:
            answer = input(f"Угадай слово № {i} >>>> {user_test_word}: ").lower().strip()
            if answer != "":
                break

        # Пользователь угадал слово, увеличиваем счетчик бонусов
        if answer == word:
            print(f"{TRUE_ANSWER_MSG}")
            total += BONUS
        # Пользователь не угадал слово ...
        else:
            print(f"Неверно! Правильный ответ – {word}.")

    # Сохраняем статистику пользователя в файл
    save_play_history(user_name=user_name, score=total)

    # Получаем статистику пользователя за предыдущие игры
    user_stat_dict = read_user_history(user_name=user_name)

    # И выводим ее на печать
    print("*" * 20)
    print(f"Всего игр сыграно: {user_stat_dict['total plays']}")
    print(f"Максимальный рекорд: {user_stat_dict['best result']}")

    # Прощаемся с пользователем
    input(f"{user_name}, cпасибо за игру!!!. Нажмите Enter для завершения ....")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.system('cls')
    main()
