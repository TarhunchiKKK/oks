import math
import random
import time
from PyQt5 import QtWidgets
from PyQt5.QtSerialPort import QSerialPort

collision_window_backoff: float = 0.04
max_counter: int = 16

def get_backoff(n: int) -> float:
    k: int = n
    if n > 10:
        k = 10
    return random.random() * math.pow(2, k)


def make_backoff(n: int) -> None:
    backoff: float = get_backoff(n)
    time.sleep(backoff / 100)


def is_port_free() -> bool:
    if random.random() < 0.7:
        return True
    else:
        return False
    

def has_collision() -> bool:
    if random.random() <= 0.3:
        return True
    else:
        return False
    

def wait_collision_window() -> None:
    time.sleep(collision_window_backoff)


def get_highlighted_data(data: str) -> str:
    highlighted_data: str = ""
    for ch in data:
        while not is_port_free():
            pass

        counter: int = 0
        highlighted_bit: str = ""

        wait_collision_window()
        while True:
            if has_collision():
                highlighted_bit += '+'
                counter += 1
                if counter < max_counter:
                    make_backoff(counter)
                else:
                    break
            else:
                highlighted_bit += '-'
                break

        highlighted_data += highlighted_bit + ' '

    return highlighted_data + '\n\n'


def send(data: str, append_status) -> str:
    data_to_send: str = ''
    for ch in data:
        while True:

            # ожидание когда порт станет свободным
            while not is_port_free():
                pass

            counter: int = 0

            # отправка
            data_to_send += ch
            wait_collision_window()

            if has_collision():
                data_to_send += ch
                append_status('+')
                # блокирует основной поток пока не выполнится вся асинхронка
                QtWidgets.QApplication.processEvents()

                counter += 1
                if counter < max_counter:
                    make_backoff(counter)
                else:
                    break
            else:
                append_status('-')
                QtWidgets.QApplication.processEvents()
                break
        append_status(' ')
        QtWidgets.QApplication.processEvents()

    append_status('\n\n')
    QtWidgets.QApplication.processEvents()

    return data_to_send

# 0101
# ++- +- - +++-

def send_with_collisions(data: str) -> (str, str):
    data_to_send: str = ""
    highlighted_data: str = ""
    for ch in data:
        while not is_port_free():
            pass

        counter: int = 0
        highlighted_bit: str = ""

        # port.write(ch.encode())
        data_to_send += ch
        
        wait_collision_window()
        while True:
            if has_collision():
                
                # port.write(ch.encode())
                data_to_send += ch
                
                highlighted_bit += '+'
                counter += 1
                if counter < max_counter:
                    make_backoff(counter)
                else:
                    break
            else:
                highlighted_bit += '-'
                break

        highlighted_data += highlighted_bit + ' '

    return (data_to_send, highlighted_data + '\n\n')