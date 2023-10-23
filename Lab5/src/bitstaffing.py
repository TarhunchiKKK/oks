import sys

def get_data(data: str) -> str:
    return data + (1 - len(data)) * "x"


def get_flag(data: str) -> str:
    length: int = len(data)
    binary_number: str = ""
    while length > 0:
        binary_number = str(length % 2) + binary_number
        length //= 2
    return "0" * (8 - len(binary_number)) + binary_number


def get_source_address(port_name: str) -> str:
    number: int = 0
    for i in range(len(port_name)):
        if port_name[i].isdigit():
            number = int(port_name[3::1])
            break

    binary_number: str = ""
    while number > 0:
        binary_number = str(number % 2) + binary_number
        number //= 2
    length: int = len(binary_number)
    return "0" * (4 - length) + binary_number


def bit_staffing(data: str) -> str:
    return data.replace('00000001', '000000001')


def de_bit_staffing(data: str) -> str:
    return data.replace('000000001', '00000001')


def get_highlighted_data(data: str) -> str:
    flag: str = data[0:8:1]
    fcs: str = data[-2::1]
    highlighted_data: str = data[8:-2:1].replace('000000001', '0000000[0]1')
    return flag + highlighted_data + ' ' + fcs + '\n'


def split_sended_on_cadres(data: str) -> list[str]:
    if len(data) == 0:
        return list("x")
    else:
        return list(data)


def split_recieved_on_cadres(data: str) -> list[str]:
    splited: list[str] = []
    length: int = len(data)
    step: int = 0
    if length % 19 == 0:
        step = 19
    elif length % 20 == 0:
        step = 20
    start: int = 0
    while start < length:
        splited.append(data[start:start + step:1])
        start += step
    return splited


def list_to_str(lst: list[str]) -> str:
    data: str = ""
    for i in lst:
        data += i
    return data