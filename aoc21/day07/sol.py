# -*- coding: utf-8 -*-
import numpy as np
from aocd.models import Puzzle


def part_1(data):
    a, b = max(data), min(data)
    min_fuel = 1e12
    for i in range(b, a):
        fuel = abs(data - i).sum()
        if fuel < min_fuel:
            min_fuel = fuel
    return min_fuel


def part_2(data):
    a, b = min(data), max(data)
    min_fuel = 1e12
    for i in range(a, b):
        abs_values = abs(data - i) + 1
        fuel = sum((sum(i for i in range(j)) for j in abs_values))
        if fuel < min_fuel:
            min_fuel = fuel
    return min_fuel


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=7)
    for line in puzzle.input_data.split("\n"):
        positions = np.array([int(i) for i in line.split(",")])

    res = part_1(positions)
    print(res)

    res = part_2(positions)
    print(res)
