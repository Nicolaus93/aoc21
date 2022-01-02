# -*- coding: utf-8 -*-
from collections import defaultdict

from aocd.models import Puzzle


def part_1(node, current_path, paths=0):
    if node == "end":
        return 1

    for neighbor in graph[node]:
        new_path = current_path | {neighbor}
        if not neighbor.isupper():
            if neighbor in current_path:
                continue
        paths += part_1(neighbor, new_path)
    return paths


def part_2(node, current_path, small_twice, paths=0):
    if node == "end":
        return 1

    for neighbor in graph[node]:
        new_path = current_path | {neighbor}
        if not neighbor.isupper():
            if neighbor in current_path:
                if small_twice or neighbor == "start":
                    continue
                else:
                    paths += part_2(neighbor, new_path, True)
                    continue
        paths += part_2(neighbor, new_path, small_twice)
    return paths


def viz_paths(node, current_path, small_twice, paths=0):
    if node == "end":
        print(current_path)
        return 1

    for neighbor in graph[node]:
        new_path = current_path + [neighbor]
        if not neighbor.isupper():
            if neighbor in current_path:
                if neighbor == "start" or len(small_twice) > 0:
                    continue
                else:
                    new_small_twice = [neighbor]
                    paths += viz_paths(neighbor, new_path, new_small_twice)
                    continue
        paths += viz_paths(neighbor, new_path, small_twice)
    return paths


if __name__ == "__main__":
    # test input
    graph = defaultdict(set)
    with open("text.txt") as f:
        for line in f:
            nodes = [i for i in line.strip().split("-")]
            graph[nodes[0]].add(nodes[1])
            graph[nodes[1]].add(nodes[0])
    viz_paths("start", ["start"], list())

    # real puzzle
    puzzle = Puzzle(year=2021, day=12)
    graph = defaultdict(set)
    for line in puzzle.input_data.split("\n"):
        nodes = [i for i in line.split("-")]
        graph[nodes[0]].add(nodes[1])
        graph[nodes[1]].add(nodes[0])

    distinct_paths = part_1("start", {"start"})
    print("part 1:", distinct_paths)

    res = part_2("start", {"start"}, False)
    print("part 2:", res)
