# -*- coding: utf-8 -*-
from itertools import product

from aocd.models import Puzzle

NEIGHBORS = [i for i in product((-1, 0, 1), (-1, 0, 1))]


def solve(data, algo, steps, debug=False):
    pad = 2
    for it in range(steps):
        min_rows = min(data, key=lambda x: x[0])[0] - pad
        min_cols = min(data, key=lambda x: x[1])[1] - pad
        max_rows = max(data, key=lambda x: x[0])[0] + pad
        max_cols = max(data, key=lambda x: x[1])[1] + pad
        new_data = set()
        for i in range(min_rows, max_rows):
            for j in range(min_cols, max_cols):
                algo_pos = ""
                for neigh in NEIGHBORS:
                    idxs = (i + neigh[0], j + neigh[1])
                    if (
                        0 <= idxs[0] <= max_rows - pad
                        and 0 <= idxs[1] <= max_cols - pad
                    ):
                        if idxs in data:
                            algo_pos += "1"
                        else:
                            algo_pos += "0"
                    else:
                        algo_pos += "0" if it % 2 == 0 else "1"
                algo_pos = int(algo_pos, 2)
                if algo[algo_pos] == "#":
                    new_data.add((i, j))
        data = {(i - min_rows, j - min_cols) for i, j in new_data}
        if debug:
            print(it, sorted(data, key=lambda x: (x[0], x[1])))
    return data


if __name__ == "__main__":
    # test_puzzle
    input_algo = None
    with open("test.txt") as f:
        for pos, line in enumerate(f):
            line = line.strip()
            if pos == 0:
                input_algo = line
            elif len(line) == 0:
                input_image = set()
                dense_image = []
            else:
                dense_image.append([1 if char == "#" else 0 for char in line])
                for col, char in enumerate(line):
                    if char == "#":
                        input_image.add((pos - 2, col))

    res = solve(input_image, input_algo, 2, debug=True)
    print(f"test part 1: {len(res)}")
    res = solve(input_image, input_algo, 50, debug=False)
    print(f"test part 2: {len(res)}")

    # real puzzle
    input_algo = None
    puzzle = Puzzle(year=2021, day=20)
    for pos, line in enumerate(puzzle.input_data.split("\n")):
        line = line.strip()
        if pos == 0:
            input_algo = line
        elif len(line) == 0:
            input_image = set()
        else:
            for col, char in enumerate(line):
                if char == "#":
                    input_image.add((pos - 2, col))

    iterations = 2
    res = solve(input_image, input_algo, iterations, debug=False)
    print("part1: ", len(res))
    iterations = 50
    res = solve(input_image, input_algo, iterations, debug=False)
    print("part2: ", len(res))
