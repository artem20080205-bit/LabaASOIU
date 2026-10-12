"""Объектно-ориентированное решение биквадратного уравнения."""

from math import sqrt
from common import read_coefficients, print_result


class BiquadraticEquation:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def discriminant(self):
        return self.b * self.b - 4 * self.a * self.c

    def solve(self):
        a, b, c = self.a, self.b, self.c
        if a == 0:
            if b == 0:
                return None if c == 0 else []
            t_values = [-c / b]
        else:
            d = self.discriminant()
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
    equation = BiquadraticEquation(*read_coefficients())
    print_result(equation.a, equation.b, equation.c, equation.solve())
