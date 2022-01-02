# -*- coding: utf-8 -*-
from itertools import product

from part1 import solve


def part_2(target_area, max_vel):
    count = 0
    temp = set()
    vel = range(-max_vel, max_vel)
    for i, j in product(vel, vel):
        res = solve(target_area, i, j)
        if res != -1:
            temp.add((i, j))
            count += 1
    return count


if __name__ == "__main__":
    # test_puzzle
    area = {"x": (20, 30), "y": (-10, -5)}
    sol = part_2(area, 45)
    print(sol)

    # real puzzle
    area = {"x": (138, 184), "y": (-125, -71)}
    sol = part_2(area, 200)
    print("part 2: ", sol)
