"""Процедурное решение биквадратного уравнения."""

from math import sqrt
from common import read_coefficients, print_result


def solve(a, b, c):
    # Замена t = x^2 сводит уравнение к квадратному.
    if a == 0:
        if b == 0:
            return None if c == 0 else []
        t_values = [-c / b]
    else:
        d = b * b - 4 * a * c
        if d < 0:
            return []
        if d == 0:
            t_values = [-b / (2 * a)]
        else:
            t_values = [(-b - sqrt(d)) / (2 * a),
                        (-b + sqrt(d)) / (2 * a)]

    roots = set()
    for t in t_values:
        if t == 0:
            roots.add(0.0)
        elif t > 0:
            roots.add(-sqrt(t))
            roots.add(sqrt(t))
    return sorted(roots)


if __name__ == "__main__":
    a, b, c = read_coefficients()
    print_result(a, b, c, solve(a, b, c))
