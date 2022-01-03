# -*- coding: utf-8 -*-
import numpy as np
from aocd.models import Puzzle

puzzle = Puzzle(year=2021, day=4)
tensor = []
mat = []
counter = 0
# for pos, line in enumerate(puzzle.input_data.split("\n")):
#     if pos == 0:
#         nums = [int(i) for i in line.split(",")]
#     elif len(line) < 1:
#         continue
#     else:
#         row = np.array([int(i) for i in line.split()])
#         mat.append(row)
#         counter += 1
#         if counter == 5:
#             tensor.append(np.array(mat))
#             mat = []
#             counter = 0

with open("input.txt") as f:
    for pos, line in enumerate(f):
        if pos == 0:
            nums = [int(i) for i in line.strip().split(",")]
        elif len(line) < 2:
            counter = 0
            mat = []
        else:
            row = np.array([int(i) for i in line.strip().split()])
            mat.append(row)
            counter += 1
            if counter == 5:
                tensor.append(np.array(mat))

tensor = np.array(tensor)
print(tensor.shape)
marked = np.zeros_like(tensor)
winners = set()
for n in nums:
    i_s, j_s, k_s = np.where(tensor == n)
    for i, j, k in zip(i_s, j_s, k_s):
        marked[i, j, k] = 1
        if marked[i, j, :].sum() == 5 or marked[i, :, k].sum() == 5:
            score_idxs = np.where(marked[i] == 0)
            xs, ys = score_idxs
            zs = [i] * len(xs)
            score = tensor[zs, xs, ys].sum() * n
            print("score: ", score)

            # update winners
            winners.add(i)
            boards_completed = len(winners)
            if boards_completed == len(tensor):
                print("final score: ", score)
                exit(0)
