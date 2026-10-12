"""Общие функции ввода и вывода для трех программ."""

import math
import sys


def read_coefficients():
    values = []
    for index, name in enumerate(("A", "B", "C"), start=1):
        text = sys.argv[index] if index < len(sys.argv) else None
        while True:
            if text is None:
                text = input(f"Введите {name}: ")
            try:
                value = float(text)
                if not math.isfinite(value):
                    raise ValueError
                values.append(value)
                break
            except ValueError:
                print(f"Ошибка: {name} должен быть конечным действительным числом.")
                text = None
    return tuple(values)


def print_result(a, b, c, result):
    print(f"Уравнение: ({a:g})*x^4 + ({b:g})*x^2 + ({c:g}) = 0")
    print(f"Дискриминант D = {b * b - 4 * a * c:g}")
    if result is None:
        print("Любое действительное число является корнем.")
    elif not result:
        print("Действительных корней нет.")
    else:
        print("Действительные корни:", "; ".join(f"{x:g}" for x in result))
