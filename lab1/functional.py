"""Функциональное решение с сопоставлением с образцом."""

from math import sqrt
from common import read_coefficients, print_result


def roots_from_t(t):
    match t:
        case 0:
            return (0.0,)
        case value if value > 0:
            return (-sqrt(value), sqrt(value))
        case _:
            return ()


def solve(a, b, c):
    # Чистая функция: результат зависит только от коэффициентов.
    match (a, b, c):
        case (0, 0, 0):
            return None
        case (0, 0, _):
            return []
        case (0, _, _):
            t_values = (-c / b,)
        case _:
            d = b * b - 4 * a * c
            match d:
                case value if value < 0:
                    return []
                case 0:
                    t_values = (-b / (2 * a),)
                case _:
                    t_values = ((-b - sqrt(d)) / (2 * a),
                                (-b + sqrt(d)) / (2 * a))

    # map преобразует корни t в корни x, set убирает повторы.
    return sorted({x for group in map(roots_from_t, t_values)
                   for x in group})


if __name__ == "__main__":
    a, b, c = read_coefficients()
    print_result(a, b, c, solve(a, b, c))
