# -*- coding: utf-8 -*-
import numpy as np
from aocd.models import Puzzle

puzzle = Puzzle(year=2021, day=5)
coords = []
max_point = 0
for line in puzzle.input_data.split("\n"):
    current_points = []
    for points in line.split("->"):
        for xy in points.split(","):
            current_points.append(int(xy))
            if int(xy) > max_point:
                max_point = int(xy)
    coords.append(current_points)

world = np.zeros((max_point + 1, max_point + 1), dtype=int)
for points in coords:
    if points[0] == points[2]:
        ys = [points[1], points[3]]
        y1, y2 = min(ys), max(ys)
        world[y1 : y2 + 1, points[0]] += 1
    elif points[1] == points[3]:
        xs = [points[0], points[2]]
        x1, x2 = min(xs), max(xs)
        world[points[1], x1 : x2 + 1] += 1
    else:
        xs = [points[0], points[2]]
        ys = [points[1], points[3]]
        x1, x2 = min(xs), max(xs)
        y1, y2 = min(ys), max(ys)
        angle = (ys[1] - ys[0]) / (xs[1] - xs[0])
        if angle > 0:
            for i, j in zip(range(x1, x2 + 1), range(y1, y2 + 1)):
                world[j, i] += 1
        else:
            for i, j in zip(range(x1, x2 + 1), reversed(range(y1, y2 + 1))):
                world[j, i] += 1

max_overlap = world.max()
score = len(np.where(world > 1)[0])
print(score)
