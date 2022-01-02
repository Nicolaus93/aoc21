# -*- coding: utf-8 -*-
from aocd.models import Puzzle

SYMBOLS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
NEW_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def part_1(data):
    score = 0
    queue = []
    for pattern in data:
        for symbol in pattern:
            if symbol in SYMBOLS:
                queue = [symbol] + queue
            else:
                matching_char = queue.pop(0)
                if SYMBOLS[matching_char] != symbol:
                    score += SCORES[symbol]
                    break

    return score


def part_2(data):
    scores = []
    for pattern in data:
        queue = []
        corrupted = False
        for symbol in pattern:
            if symbol in SYMBOLS:
                queue = [symbol] + queue
            else:
                matching_char = queue.pop(0)
                if SYMBOLS[matching_char] != symbol:
                    corrupted = True
                    break

        if not corrupted:
            completion = [SYMBOLS[i] for i in queue]
            score = 0
            for char in completion:
                score *= 5
                score += NEW_SCORES[char]
            scores.append(score)

    scores = sorted(scores)
    length = len(scores)
    return scores[length // 2]


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=10)
    lines = []
    for line in puzzle.input_data.split("\n"):
        lines.append(line)

    res = part_1(lines)
    print(res)

    res = part_2(lines)
    print(res)
