# -*- coding: utf-8 -*-
from copy import deepcopy

from aocd.models import Puzzle
from tqdm import trange


def move(row, where):
    new_row = deepcopy(row)
    for loc, couple in enumerate(zip(row, row[1:])):
        c1, c2 = couple
        if c1 == where and c2 == ".":
            new_row[loc] = "."
            new_row[loc + 1] = where
    if row[-1] == where and row[0] == ".":
        new_row[-1] = "."
        new_row[0] = where
    return new_row


def solve(input_f=None, debug=False):
    if not input_f:
        puzzle = Puzzle(year=2021, day=25)
        data = puzzle.input_data.split("\n")
    else:
        data = open(input_f).readlines()
    processed_data = []
    for line in data:
        processed_data.append([i for i in line.strip()])

    data = processed_data
    if debug:
        for row in data:
            print("".join(row))
        print()

    rows = len(data)
    cols = len(data[0])
    for step in trange(1000):
        if debug:
            print(f"After step {step+1}:")
        new_data = [["."] * cols for _ in range(rows)]
        # move left
        for pos, row in enumerate(data):
            new_row = move(row, ">")
            new_data[pos] = new_row

        # move down
        for j in range(cols):
            col = [new_data[i][j] for i in range(rows)]
            new_col = move(col, "v")
            # update col
            for i in range(rows):
                new_data[i][j] = new_col[i]

        if data == new_data:
            break
        data = new_data

        if debug:
            for row in data:
                print("".join(row))
            print()
    return step + 1


if __name__ == "__main__":
    # test_puzzle
    res = solve("test.txt")
    print("part1: ", res)

    # real puzzle
    res = solve()
    print(res)
