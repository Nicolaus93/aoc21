# -*- coding: utf-8 -*-
from aocd.models import Puzzle

ENCODE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def decode(data):
    if len(data) <= 6:
        return 0
    version = int(data[:3], 2)
    type_id = int(data[3:6], 2)
    version_sum = version
    pos = 6
    if type_id == 4:
        num = ""
        while pos < len(data):
            chunk = data[pos : pos + 5]
            num += chunk[1:]
            pos += 5
            if chunk[0] == "0":
                break
        real_num = int(num, 2)
        print(real_num)
    else:
        length_type_id = data[pos]
        pos += 1
        if length_type_id == "0":
            subpackets_length = int(data[pos : pos + 15], 2)
            pos += 15
            end = pos + subpackets_length
            while pos < end:
                increase_version, increase_pos = decode(data[pos:])
                version_sum += increase_version
                pos += increase_pos
        else:
            tot_subpackets = int(data[pos : pos + 11], 2)
            pos += 11
            for j in range(tot_subpackets):
                increase_version, increase_pos = decode(data[pos:])
                version_sum += increase_version
                pos += increase_pos

    return version_sum, pos


if __name__ == "__main__":
    # test_puzzle
    test_data = ""
    with open("test.txt") as f:
        for pos, line in enumerate(f):
            for i in line.strip():
                test_data += ENCODE[i]

            res, _ = decode(test_data)
            print(f"test{pos}: {res}")

    # real puzzle
    processed_data = ""
    puzzle = Puzzle(year=2021, day=16)
    for line in puzzle.input_data.split("\n"):
        for i in line:
            processed_data += ENCODE[i]

    res, _ = decode(processed_data)
    print("part1: ", res)
