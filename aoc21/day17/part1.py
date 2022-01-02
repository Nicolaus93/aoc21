# -*- coding: utf-8 -*-
from itertools import product


def solve(target_area, vel_x, vel_y, debug=False):

    x, y = (0, 0)
    x_min = min(target_area["x"])
    x_max = max(target_area["x"])
    y_min = min(target_area["y"])
    y_max = max(target_area["y"])
    highest_pos = 0
    if x_max > 0:
        while not (x >= x_min and y <= y_max):
            if debug:
                print(x, y)
            x += vel_x
            y += vel_y
            if y > highest_pos:
                highest_pos = y

            if x > x_max or y < y_min:
                return -1
            if x_min <= x <= x_max and y_max >= y >= y_min:
                return highest_pos

            if vel_x > 0:
                vel_x -= 1
            elif vel_x < 0:
                vel_x += 1
            vel_y -= 1

    return -1


def part_1(target_area, max_vel):
    res = solve(area, 0, 0)
    vel = range(1, max_vel + 1)
    for i, j in product(vel, vel):
        new_res = solve(target_area, i, j)
        if new_res > res:
            res = new_res
    return res


if __name__ == "__main__":
    # test_puzzle
    area = {"x": (20, 30), "y": (-10, -5)}
    sol = part_1(area, 10)
    print(sol)

    # real puzzle
    area = {"x": (138, 184), "y": (-125, -71)}
    sol = part_1(area, 200)
    print("part 1: ", sol)
