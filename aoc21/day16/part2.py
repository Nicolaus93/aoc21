# -*- coding: utf-8 -*-
from aocd.models import Puzzle
from part1 import ENCODE


def decode(data):
    if len(data) <= 6:
        return 0
    # version = int(data[:3], 2)
    type_id = int(data[3:6], 2)
    pos = 6
    if type_id == 4:
        num = ""
        while pos < len(data):
            chunk = data[pos : pos + 5]
            num += chunk[1:]
            pos += 5
            if chunk[0] == "0":
                break
        value = int(num, 2)
    else:
        length_type_id = data[pos]
        pos += 1
        values = []
        if length_type_id == "0":
            subpackets_length = int(data[pos : pos + 15], 2)
            pos += 15
            end = pos + subpackets_length
            while pos < end:
                subpacket_val, increase_pos = decode(data[pos:])
                values.append(subpacket_val)
                pos += increase_pos
        else:
            tot_subpackets = int(data[pos : pos + 11], 2)
            pos += 11
            for j in range(tot_subpackets):
                subpacket_val, increase_pos = decode(data[pos:])
                values.append(subpacket_val)
                pos += increase_pos

        if type_id == 0:
            value = sum(values)
        elif type_id == 1:
            value = 1
            for num in values:
                value *= num
        elif type_id == 2:
            value = min(values)
        elif type_id == 3:
            value = max(values)
        elif type_id == 5:
            assert (
                len(values) == 2
            ), "greater than is supposed to have only 2 subpackets!"
            value = 1 if values[0] > values[1] else 0
        elif type_id == 6:
            assert len(values) == 2, "less than is supposed to have only 2 subpackets!"
            value = 1 if values[0] < values[1] else 0
        elif type_id == 7:
            assert len(values) == 2, "equal to is supposed to have only 2 subpackets!"
            value = 1 if values[0] == values[1] else 0
        else:
            raise ValueError("type id not recognized!")

    return value, pos


if __name__ == "__main__":
    # test_puzzle
    with open("test.txt") as f:
        for j, line in enumerate(f):
            test_data = ""
            for i in line.strip():
                test_data += ENCODE[i]

            res, _ = decode(test_data)
            print(f"test{j}: {res}")

    # real puzzle
    processed_data = ""
    puzzle = Puzzle(year=2021, day=16)
    for line in puzzle.input_data.split("\n"):
        for i in line:
            processed_data += ENCODE[i]

    res, _ = decode(processed_data)
    print("part1: ", res)
