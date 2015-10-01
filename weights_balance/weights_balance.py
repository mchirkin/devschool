"""
HeadHunter DEVSchool
Задача       : Баланс весов
Автор решения: Чиркин М.В.
Дата         : 01.10.2015
"""


import itertools


def search_equal_weights(weight_combinations, weight_for_search):
    """
    Поиск заданной суммы весов в списке
    возможных комбинаций предметов
    """

    for w in weight_combinations:
        if sum(w) == weight_for_search:
            return w

    return False


items_number = int(input("Enter number of items: "))
items_list = list()

for i in range(1, items_number+1):
    print("#", i, " Enter item's weight")
    items_list.append(int(input("weight = ")))

# Находим сумму весов всех предметов
weights_sum = sum(items_list)

# Если сумма весов предметов нечетная,
# то на две равные части предметы разделить нельзя
if 0 == weights_sum % 2:
    # Суммарный вес одной из частей предметов
    weight_for_search = weights_sum // 2
    # Будем искать сумму весов только в комбинациях,
    # состоящих не менее чем из половины предметов
    middle_index = items_number // 2

    for i in range(items_number - 1, middle_index, -1):
        # Находим все возможные комбинации предметов,
        # состоящие из i элементов
        weight_combinations = list(itertools.combinations(items_list, i))
        # Ищем в найденных комбинациях искомый вес
        weight_comb = search_equal_weights(weight_combinations, weight_for_search)

        # Если искомый вес найден,
        # то из исходного списка предметов удалаем найденные
        if weight_comb:
            for w in weight_comb:
                items_list.remove(w)
            # Выводим полученный результат
            print(weight_comb, ' - ', tuple(items_list))
            break

print(["no", "yes"][weights_sum >= 100])
