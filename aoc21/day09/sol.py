# -*- coding: utf-8 -*-
import numpy as np
from aocd.models import Puzzle


def part_1(data):
    rows, cols = data.shape
    lowest = []
    for row in range(rows):
        for col in range(cols):
            loc = data[row, col]
            left = data[row, col - 1] if col > 0 else 10
            right = data[row, col + 1] if col < cols - 1 else 10
            up = data[row - 1, col] if row > 0 else 10
            down = data[row + 1, col] if row < rows - 1 else 10
            if loc < left and loc < right and loc < up and loc < down:
                lowest.append(loc)
    return sum(1 + i for i in lowest)


def part_2(data):
    rows, cols = data.shape
    basins = []
    for row in range(rows):
        for col in range(cols):
            loc = data[row, col]
            if loc == 9:
                continue
            current_basin = set()
            current_basin_size = 0
            current_basin.add((row, col))
            while current_basin:
                x, y = current_basin.pop()
                current_basin_size += 1
                data[x, y] = 9
                left = data[x, y - 1] if y > 0 else 10
                if left < 9:
                    current_basin.add((x, y - 1))
                right = data[x, y + 1] if y < cols - 1 else 10
                if right < 9:
                    current_basin.add((x, y + 1))
                up = data[x - 1, y] if x > 0 else 10
                if up < 9:
                    current_basin.add((x - 1, y))
                down = data[x + 1, y] if x < rows - 1 else 10
                if down < 9:
                    current_basin.add((x + 1, y))
            basins.append(current_basin_size)

    basins = sorted(basins, reverse=True)
    score = 1
    for i in range(3):
        score *= basins[i]
    return score


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=9)
    locations = []
    for line in puzzle.input_data.split("\n"):
        processed_data = np.array([int(i) for i in line])
        locations.append(processed_data)

    locations = np.array(locations)
    res = part_1(locations)
    print(res)

    res = part_2(locations)
    print(res)
