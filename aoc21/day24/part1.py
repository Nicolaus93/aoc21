# -*- coding: utf-8 -*-
from aocd.models import Puzzle


def solve(data):
    return -1


if __name__ == "__main__":
    # test_puzzle
    test_data = []
    with open("test.txt") as f:
        for line in f:
            test_data.append(line.strip())

    res = solve(test_data)
    print("part1: ", res)

    # real puzzle
    processed_data = []
    puzzle = Puzzle(year=2021, day=24)
    for line in puzzle.input_data.split("\n"):
        processed_data.append([int(i) for i in line.split(",")])

    res = solve(processed_data)
    print(res)
