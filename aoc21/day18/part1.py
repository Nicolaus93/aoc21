# -*- coding: utf-8 -*-
import typing
from itertools import combinations

from aocd.models import Puzzle


def add(data, number, side):
    if isinstance(data, int):
        return data + number
    if side == "left":
        res = add(data[0], number, "left")
        data[0] = res
    else:
        res = add(data[1], number, "right")
        data[1] = res
    return data


def explode(
    data: typing.List, depth: int = 0, left: int = -1, right: int = -1
) -> typing.Tuple[int, int]:
    if (left, right) == (0, 0):
        return 0, 0
    if isinstance(data, int):
        return left, right

    for pos, item in enumerate(data):
        if depth == 3:
            if isinstance(item, int):
                continue
            left, right = item
            data[pos] = 0
            if pos == 0:
                # add right
                data[1] = add(data[1], right, "left")
                right = 0
            else:
                # add left
                data[0] = add(data[0], left, "right")
                left = 0
            return left, right

        left, right = explode(item, depth=depth + 1)
        # add remainder
        if left > 0:
            if pos == 1:
                data[0] = add(data[0], left, "right")
                left = 0
            return left, right
        elif right > 0:
            if pos == 0:
                data[1] = add(data[1], right, "left")
                right = 0
            return left, right
        elif (left, right) == (0, 0):
            return left, right
    return left, right


def split(data: typing.List, depth: int = 0, split_done: bool = False) -> bool:
    if split_done:
        return split_done
    if isinstance(data, int):
        return split_done

    for pos, item in enumerate(data):
        if isinstance(item, int):
            if item >= 10:
                first = second = item // 2
                if item % 2 == 1:
                    second += 1
                data[pos] = [first, second]
                return True
        split_done = split(item, depth=depth + 1)
        if split_done:
            return split_done
    return split_done


class SnailFish:
    def __init__(self, number=None):
        self.number = number

    def reduce(self):
        keep_reducing = explode(self.number)
        while keep_reducing != (-1, -1):
            keep_reducing = explode(self.number)
            if keep_reducing == (-1, -1):
                has_been_split = split(self.number)
                if has_been_split:
                    keep_reducing = (0, 0)

    def magnitude(self, data=None):
        if data is None:
            data = self.number
        if isinstance(data, int):
            return data

        left = self.magnitude(data[0])
        right = self.magnitude(data[1])
        return 3 * left + 2 * right

    def add(self, other):
        self.number = [self.number, other]

    def solve(self, input_f=None):
        if not input_f:
            puzzle = Puzzle(year=2021, day=18)
            puzzle_data = puzzle.input_data.split("\n")
        else:
            puzzle_data = open(input_f).readlines()
        for pos, line in enumerate(puzzle_data):
            if pos == 0:
                self.number = eval(line.strip())
            else:
                self.add(eval(line.strip()))
                self.reduce()
        print(f"part1: {self.magnitude(self.number)}")

        max_magnitude = 0
        for i, j in combinations(puzzle_data, 2):
            for n1, n2 in [(i, j), (j, i)]:
                self.number = eval(n1.strip())
                self.add(eval(n2.strip()))
                self.reduce()
                new_magn = self.magnitude()
                max_magnitude = max(max_magnitude, new_magn)
        print(f"part2: {max_magnitude}")


if __name__ == "__main__":
    snail = SnailFish()
    print("test..")
    snail.solve("test.txt")
    print("real puzzle..")
    snail.solve()
