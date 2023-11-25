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
    counter: int = 0
    staffed: str = ""
    for i in range(len(data)):
        staffed += data[i]
        if data[i] == "0":
            counter += 1
            if counter == 7:
                staffed += "0"
                counter = 0
        elif data[i] == "1":
            counter = 0
    return staffed


def de_bit_staffing(data: str) -> str:
    counter: int = 0
    destuffed: str = ""
    for i in data:
        if i == "0":
            counter += 1
            if counter != 8:
                destuffed += i
            else:
                counter = 0
        elif i == "1" or i == "x":
            destuffed += i
            counter = 0
    return destuffed
    # return data.replace('000000001', '00000001')

def get_highlighted_bits(data: str) -> str:
    # counter: int = 0
    # highlighted_data: str = ""
    # for i in range(len(data)):
    #     if data[i] == "0":
    #         counter += 1
    #     elif data[i] == "1":
    #         counter = 0
    #
    #     if counter == 8:
    #         highlighted_data += "["
    #         highlighted_data += data[i]
    #         highlighted_data += "]"
    #         counter = 0
    #     else:
    #         highlighted_data += data[i]
    # return highlighted_data[0:-2:1] + ' ' + data[-2::1]
    return data[0:-2:1].replace('000000001', '0000000[0]1') + ' ' + data[-2::1]


def divide_str(data: str) -> list[str]:
    if len(data) == 0:
        return list("x")
    else:
        return list(data)


def split_on_packages(data: str) -> list[str]:
    # splited: list[str] = []
    # length: int = len(data)
    # step: int = 0
    #
    # if length % 20 == 0:
    #     step = 20
    # else:
    #     step = 19
    # start: int = 0
    # while start < length:
    #     if start + step:
    #         splited.append(data[start::1])
    #         break
    #     splited.append(data[start:start + step:1])
    #     start += step
    # return splited

    splited: list[str] = []
    length: int = len(data)
    step: int = 8

    start: int = 0
    while True:
        position: int = data.find('00000001', start)
        if position == -1:
            break

        start = position
        end: int = data.find('00000001', start + step * 2)
        if end == -1:
            splited.append(data[start::1])
            break

        if end >= length:
            break

        splited.append(data[start:end:1])

        start = end

    return splited




def list_to_str(lst: list[str]) -> str:
    data: str = ""
    for i in lst:
        data += i
    return data



# lst: list[str] = split_on_packages("00010001000001001111")
#
# # lst: list[str] = split_on_packages("00000001000000001111")
# for l in lst:
#     print(l)