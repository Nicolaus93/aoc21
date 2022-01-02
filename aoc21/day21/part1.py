# -*- coding: utf-8 -*-
from collections import namedtuple
from copy import deepcopy
from functools import lru_cache
from itertools import product


def solve(pos_1, pos_2):
    player_1 = dict(pos=pos_1, score=0)
    player_2 = dict(pos=pos_2, score=0)
    die = 1
    first_plays = True
    count = 0
    while player_1["score"] < 1000 and player_2["score"] < 1000:
        increase = 3 * die + 3
        if first_plays:
            player_1["pos"] = (player_1["pos"] + increase) % 10
            player_1["score"] += player_1["pos"] if player_1["pos"] != 0 else 10
        else:
            player_2["pos"] = (player_2["pos"] + increase) % 10
            player_2["score"] += player_2["pos"] if player_2["pos"] != 0 else 10
        die += 3
        first_plays = not first_plays
        count += 3
    return player_1, player_2, count


Player = namedtuple("Player", "pos score")


@lru_cache(maxsize=None)
def quantum(p1, p2, first_plays):
    wins_1 = wins_2 = 0
    if p1.score >= 21:
        return 1, 0
    elif p2.score >= 21:
        return 0, 1

    if first_plays:
        player, watcher = p1, p2
    else:
        player, watcher = p2, p1

    for die_rolls in product([1, 2, 3], repeat=3):
        roll = sum(die_rolls)
        new_pos = (player.pos + roll) % 10
        score_increase = new_pos if new_pos != 0 else 10
        new_score = player.score + score_increase
        new_p = Player(new_pos, new_score)
        new_w = deepcopy(watcher)
        if first_plays:
            w1, w2 = quantum(new_p, new_w, not first_plays)
        else:
            w1, w2 = quantum(new_w, new_p, not first_plays)
        wins_1 += w1
        wins_2 += w2
    return wins_1, wins_2


if __name__ == "__main__":
    x = 10
    y = 6

    # part 1
    first, second, rolls = solve(x, y)
    print("part1:", min(first["score"], second["score"]) * rolls)

    # part 2
    pl1 = Player(x, 0)
    pl2 = Player(y, 0)
    print("part2:", max(quantum(pl1, pl2, True)))
