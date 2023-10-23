import math
import random
import time

collision_window_backoff: float = 0.05
max_counter: int = 16

def get_backoff(n: int) -> float:
    k: int = n
    if n > 10:
        k = 10
    return random.random() * math.pow(2, k)


def make_backoff(n: int) -> None:
    backoff: float = get_backoff(n)
    time.sleep(backoff / 2000)


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