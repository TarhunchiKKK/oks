import math
import random


# 0 - четное
# 1 - нечетное


def distort_data(data: str) -> str:
    if random.random() <= 0.7:
        if data[0] == "0":
            return "1" + data[1::1]
        elif data[0] == "1":
            return "0" + data[1::1]
    return data


#  перевод массиа символов в строку
def list_to_str(lst: list[str]) -> str:
    data: str = ""
    for i in lst:
        data += i
    return data


# получить количесвт оконтрольных бит в зависимости от длины поля data
def get_fcs_length(number: int) -> int:
    for i in range(0, 10):
        if math.pow(2, i) > number:
            return i + 1
    return -1


# получение fcs
def get_fcs(data: str) -> str:
    length: int = len(data)
    fcs_length: int = get_fcs_length(length)
    fcs: str = ""

    # выравнивание индексов
    data = "x" + data

    # вставка контрольных битов
    positions_to_insert: list[int] = get_positions_to_insert(fcs_length)
    data_list: list[str] = list(data)
    for position in positions_to_insert:
        data_list.insert(position, "0")
    data = list_to_str(data_list)

    # вычисление контрольных бит
    for position in positions_to_insert:
        fcs += get_control_bit_value(data, position)

    return fcs


# получить позиции для вставки
def get_positions_to_insert(power: int) -> list[int]:
    positions: list[int] = []
    for i in range(power):
        positions.append(int(math.pow(2, i)))
    return positions


# вычисление значения контрольного бита
def get_control_bit_value(data: str, position: int) -> str:
    counter: int = 0
    i: int = position
    length: int = len(data)
    while i < length:
        j: int = 0

        # контролируемые биты
        while j < position and i < length:
            if data[i] == "1":
                counter += 1
            # print(i)
            i += 1
            j += 1

        j = 0
        # пропустить биты
        while j < position and i < length:
            i += 1
            j += 1

    if counter % 2 == 0:
        return "0"
    else:
        return "1"



# проверка на несоответствие полученны и вычисленных контрольных бит
def check(data: str, fcs: str) -> bool:
    # выравнивание индексов
    data = "x" + data
    fcs_length: int = len(fcs)

    # вставка контроьных битов в строку
    positions_to_insert: list[int] = get_positions_to_insert(fcs_length)
    data_list: list[str] = list(data)
    for position in positions_to_insert:
        data_list.insert(position, "0")
    data = list_to_str(data_list)

    # вычисление контрольных битов
    new_fcs: str = ""
    for position in positions_to_insert:
        new_fcs += get_control_bit_value(data, position)

    return fcs == new_fcs


# исправление неправильного бита
def fix(data: str, fcs: str) -> str:
    # выравнивание индексов
    data = "x" + data
    fcs_length: int = len(fcs)

    # вставка контрольных битов в нужные позиции
    positions_to_insert: list[int] = get_positions_to_insert(fcs_length)
    data_list: list[str] = list(data)
    for position in positions_to_insert:
        data_list.insert(position, "0")
    data = list_to_str(data_list)

    # поиск позиций несовпадающих битов
    different_control_bits_indexes: list[int] = []
    for i in range(len(positions_to_insert)):
        control_bit_value = get_control_bit_value(data, positions_to_insert[i])
        if fcs[i] != control_bit_value:
            different_control_bits_indexes.append(i)

    # исправление неправильного бита, если таковой имеется
    if len(different_control_bits_indexes) != 0:

        # вычисление позиции неправильного бита
        different_control_bit_index: int = 0
        for i in different_control_bits_indexes:
            different_control_bit_index += i + 1    # + 1 т.к индексация fcs начинается с нуля

        # инвертирование неправильного бита
        data_list = list(data)
        if data_list[different_control_bit_index] == "0":
            data_list[different_control_bit_index] = "1"
        else:
            data_list[different_control_bit_index] = "0"

    # удаление контрольных битов в порядке, обратном вставке
    positions_to_insert.reverse()
    for i in positions_to_insert:
        data_list[i] = ""

    data = list_to_str(data_list)
    return data[1::1]                               # убрать первый символ (символ для выравнивания)


