# -*- coding: utf-8 -*-
from collections import Counter

from aocd.models import Puzzle
from tqdm import trange


def solve(data, instr, steps):

    for _ in trange(steps):
        couples = [(i, j) for (i, j) in zip(data, data[1:])]
        new_data = ""
        for pos, couple in enumerate(couples):
            if pos == 0:
                new_data += couple[0] + instr["".join(couple)] + couple[1]
            else:
                new_data += instr["".join(couple)] + couple[1]
        data = new_data
    count = Counter(data)
    occurrences = count.most_common()
    return occurrences[0][1] - occurrences[-1][1]


def smart_solve(data, instr, steps):

    couples = Counter([(i, j) for (i, j) in zip(data, data[1:])])
    first_letter = data[0]
    last_letter = data[-1]
    for _ in trange(steps):
        new_couples = Counter()
        for couple in couples:
            new_letter = instr["".join(couple)]
            left, right = couple
            new_couples[(left, new_letter)] += couples[couple]
            new_couples[(new_letter, right)] += couples[couple]
        couples = new_couples

    occurrences = Counter()
    for couple in couples:
        i, j = couple
        count = couples[couple]
        occurrences[i] += count
        occurrences[j] += count

    for letter in occurrences:
        if letter == first_letter:
            occurrences[letter] += 1
        if letter == last_letter:
            occurrences[letter] += 1
        occurrences[letter] = occurrences[letter] // 2
    count = occurrences.most_common()
    return count[0][1] - count[-1][1]


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=14)
    rules = dict()
    for pos, line in enumerate(puzzle.input_data.split("\n")):
        if pos == 0:
            start = [i for i in line]
        else:
            if len(line) == 0:
                continue
            rule = line.split(" -> ")
            rules[rule[0]] = rule[1]

    res = solve(start, rules, 10)
    print(res)

    res = smart_solve(start, rules, 40)
    print(res)
