import math


def code(data: str) -> str:
    length: int = len(data)
    return ""


def decode(data: str) -> str:
    length: int = len(data)
    return ""

def check(data: str) -> bool:
    return True

def nearest_power(number: int) -> int:
    for i in range(0, 10):
        if math.pow(2, i) > number:
            return i
    return -1


def list_to_str(lst: list[str]) -> str:
    data: str = ""
    for i in lst:
        data += i
    return data

print(nearest_power(3))
print(nearest_power(1))

# lst: list[str] = list("abc")

