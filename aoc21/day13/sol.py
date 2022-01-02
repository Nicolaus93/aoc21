# -*- coding: utf-8 -*-
from aocd.models import Puzzle


def visualize(data):
    max_x = max(key[0] for key in data) + 1
    max_y = max(key[1] for key in data) + 1
    vis = [[" " for _ in range(max_x)] for _ in range(max_y)]
    for point in data:
        x, y = point
        vis[y][x] = "#"
    for row in vis:
        print("".join(row))


def solve(data, fold_point, fold_direction):
    if fold_direction == "x":
        data_right = {(x - fold_point - 1, y) for (x, y) in data if x > fold_point}
        data_left = {(fold_point - x - 1, y) for (x, y) in data if x < fold_point}
        result = data_left | data_right
    elif fold_direction == "y":
        data_up = {(x, fold_point - 1 - y) for (x, y) in data if y < fold_point}
        data_down = {(x, y - fold_point - 1) for (x, y) in data if y > fold_point}
        result = data_down | data_up
    else:
        raise ValueError
    return result


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=13)
    grid = set()

    instructions = []
    for line in puzzle.input_data.split("\n"):
        line = line.strip()
        if not line.startswith("fold"):
            if len(line) == 0:
                continue
            processed_data = [int(i) for i in line.split(",")]
            i, j = processed_data
            grid.add((i, j))
        else:
            instruction = line.split(" ")
            instruction = instruction[-1].split("=")
            coord = instruction[0]
            num = int(instruction[1])
            instructions.append((num, coord))

    first_num, first_coord = instructions[0]
    res = solve(grid, first_num, first_coord)
    lets_see = False
    if lets_see:
        visualize(res)
    print("part 1:", len(res))

    for (num, coord) in instructions:
        grid = solve(grid, num, coord)
    visualize(grid)  # result is flipped!
