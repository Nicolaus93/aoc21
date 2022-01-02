# -*- coding: utf-8 -*-
from itertools import product

from aocd.models import Puzzle

STEPS = 100
NEIGHBORS = [i for i in product((-1, 0, 1), (-1, 0, 1)) if i != (0, 0)]


def part_1(data):
    score = 0
    for step in range(STEPS):
        data = [[i + 1 if i + 1 < 10 else 0 for i in row] for row in data]
        flash = [
            (row, col)
            for row in range(len(data))
            for col in range(len(data[0]))
            if data[row][col] == 0
        ]
        score += len(flash)
        visited = set(flash)
        while flash:
            i, j = flash.pop()
            for neighbor in NEIGHBORS:
                x = neighbor[0] + i
                y = neighbor[1] + j
                if x < 0 or y < 0:
                    continue
                try:
                    if (x, y) not in visited:
                        data[x][y] += 1
                        if data[x][y] == 10:
                            score += 1
                            data[x][y] = 0
                            flash.append((x, y))
                            visited.add((x, y))
                except IndexError:
                    continue
    return score


def part_2(data):
    count = 0
    while sum(i for row in data for i in row) != 0:
        count += 1
        data = [[i + 1 if i + 1 < 10 else 0 for i in row] for row in data]
        flash = [
            (row, col)
            for row in range(len(data))
            for col in range(len(data[0]))
            if data[row][col] == 0
        ]
        visited = set(flash)
        while flash:
            i, j = flash.pop()
            for neighbor in NEIGHBORS:
                x = neighbor[0] + i
                y = neighbor[1] + j
                if x < 0 or y < 0 or x >= len(data) or y >= len(data[0]):
                    continue
                if (x, y) not in visited:
                    data[x][y] += 1
                    if data[x][y] == 10:
                        data[x][y] = 0
                        flash.append((x, y))
                        visited.add((x, y))
    return count


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=11)
    octopus = []
    for line in puzzle.input_data.split("\n"):
        processed_data = [int(i) for i in line.strip()]
        octopus.append(processed_data)

    res = part_1(octopus)
    print(res)

    res = part_2(octopus)
    print(res)
