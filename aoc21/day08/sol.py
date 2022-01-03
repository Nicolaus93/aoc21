# -*- coding: utf-8 -*-
from collections import defaultdict

from aocd.models import Puzzle


def part_1(data):
    tot = 0
    for out in data:
        for pos, value in enumerate(out):
            if value == "|":
                out = out[pos + 1 :]
                break
        for i in out:
            if len(i) in {2, 3, 4, 7}:
                tot += 1
    return tot


def part_2(data):
    tot = 0
    for codes in data:
        unique_patterns = defaultdict(set)
        for pattern in codes[:10]:
            unique_patterns[len(pattern)].add(pattern)

        if len(unique_patterns[5]) != 3:
            print(codes)
            print(unique_patterns)
        if len(unique_patterns[6]) != 3:
            print(codes)
            print(unique_patterns)

        # find 1, 7, 4
        one = unique_patterns[2].pop()
        seven = unique_patterns[3].pop()
        four = unique_patterns[4].pop()

        # find 2
        for pattern in unique_patterns[5]:
            if len(set(four) & set(pattern)) == 2:
                two = pattern
                unique_patterns[5].remove(pattern)
                break

        # find 5
        for pattern in unique_patterns[5]:
            if len(set(two) - set(pattern)) == 2:
                five = pattern
                unique_patterns[5].remove(pattern)
                break

        # find 3
        assert len(unique_patterns[5]) == 1
        three = unique_patterns[5].pop()

        # find 0
        for pattern in unique_patterns[6]:
            if (
                len(set(pattern) - set(five)) == 2
                and len(set(pattern) - set(two)) == 2
                and len(set(pattern) - set(three)) == 2
            ):
                zero = pattern
                unique_patterns[6].remove(zero)
                break

        # find 9
        assert len(unique_patterns[6]) == 2
        for pattern in unique_patterns[6]:
            if len(set(one) - set(pattern)) == 1:
                six = pattern
            elif len(set(one) - set(pattern)) == 0:
                nine = pattern
            else:
                raise ValueError("AARGH!")

        eight = unique_patterns[7].pop()
        numbers = {
            tuple(sorted(zero)): 0,
            tuple(sorted(one)): 1,
            tuple(sorted(two)): 2,
            tuple(sorted(three)): 3,
            tuple(sorted(four)): 4,
            tuple(sorted(five)): 5,
            tuple(sorted(six)): 6,
            tuple(sorted(seven)): 7,
            tuple(sorted(eight)): 8,
            tuple(sorted(nine)): 9,
        }

        digit = ""
        for pattern in codes[11:]:
            digit += str(numbers[tuple(sorted(pattern))])
        tot += int(digit)
    return tot


if __name__ == "__main__":
    year = 2021
    day = 8
    puzzle = Puzzle(year=year, day=day)
    processed_data = []
    for line in puzzle.input_data.split("\n"):
        processed_data.append([i for i in line.split(" ")])

    length = dict()
    length[2] = ["1"]
    length[3] = ["7"]
    length[4] = ["4"]
    length[7] = ["8"]
    length[5] = ["2", "3", "5"]
    length[6] = ["0", "6", "9"]

    res = part_1(processed_data)
    print(res)

    res = part_2(processed_data)
    print(res)
