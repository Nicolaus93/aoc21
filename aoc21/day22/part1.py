# -*- coding: utf-8 -*-
import re

from aocd.models import Puzzle


def restrict(start, end):
    start = int(start)
    end = int(end)
    return max(start, -50), min(end + 1, 51)


def gen_cubes(some_string):
    coords = re.findall(r"-?\d+", some_string)
    x0, x1 = restrict(coords[0], coords[1])
    y0, y1 = restrict(coords[2], coords[3])
    z0, z1 = restrict(coords[4], coords[5])
    return {
        (i, j, k) for i in range(x0, x1) for j in range(y0, y1) for k in range(z0, z1)
    }


if __name__ == "__main__":
    # test_puzzle
    cubes = set()
    with open("test.txt") as f:
        for line in f:
            instr = line.strip().split()
            new_cubes = gen_cubes(instr[1])
            if instr[0] == "on":
                cubes = cubes | new_cubes
            elif instr[0] == "off":
                cubes = cubes - new_cubes
            else:
                raise ValueError
            print(len(cubes))

    print("test: ", len(cubes))

    # real puzzle
    cubes = set()
    puzzle = Puzzle(year=2021, day=22)
    for line in puzzle.input_data.split("\n"):
        instr = line.strip().split()
        new_cubes = gen_cubes(instr[1])
        if instr[0] == "on":
            cubes = cubes | new_cubes
        elif instr[0] == "off":
            cubes = cubes - new_cubes
        else:
            raise ValueError

    print("part1: ", len(cubes))
