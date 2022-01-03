# -*- coding: utf-8 -*-
from aocd.models import Puzzle

DAYS_FOR_BIRTH = 7
LAST_DAY_PART_1 = 80
LAST_DAY_PART_2 = 256


def memoize(fun):
    cache = dict()

    def memoizer(birthday, last_day):
        if birthday not in cache:
            cache[birthday] = fun(birthday, last_day)
        return cache[birthday]

    return memoizer


@memoize
def recur(birthday, last_day):
    if birthday > last_day:
        return 0
    new_born = [j + 8 for j in range(birthday + 1, last_day, DAYS_FOR_BIRTH)]
    tot = len(new_born)
    for fish_birthday in new_born:
        tot += recur(fish_birthday, last_day)
    return tot


def dp(init):
    last_day = LAST_DAY_PART_2
    borns = [0] * last_day
    for i in init:
        for day in range(i, last_day, 7):
            borns[day] += 1

    for day, new_borns in enumerate(borns):
        first_time = True
        while day < last_day:
            if first_time:
                day += 9
                first_time = False
            else:
                day += 7
            if day < last_day:
                borns[day] += new_borns
    return sum(borns) + len(init)


if __name__ == "__main__":

    # retrieve data
    puzzle = Puzzle(year=2021, day=6)
    for line in puzzle.input_data.split("\n"):
        initial_fish = [int(i) for i in line.split(",")]

    # part 2
    part_2 = len(initial_fish)
    for day_ in initial_fish:
        part_2 += recur(day_, LAST_DAY_PART_2 + 1)
    print("part 2:", part_2)

    # initial_fish = [3, 4, 3, 1, 2]
    print(dp(initial_fish))
