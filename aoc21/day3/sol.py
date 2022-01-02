# -*- coding: utf-8 -*-
from copy import deepcopy

import numpy as np

nums = []
with open("input.txt") as f:
    for line in f:
        n = [int(i) for i in (line.strip())]
        nums.append(n)

mat = np.array(nums)
most_common = np.sum(mat, axis=0) > (len(mat) // 2)
res1 = sum([2 ** pos for pos, value in enumerate(most_common[::-1]) if value])
res2 = sum([2 ** pos for pos, value in enumerate(most_common[::-1]) if not value])
print(res1 * res2)

ox = deepcopy(mat)
co2 = deepcopy(mat)

for col in range(mat.shape[1]):
    count = np.bincount(ox[:, col])
    most_common = 1 if count[1] >= count[0] else 0
    ox = ox[ox[:, col] == most_common]
    if len(ox) == 1:
        ox = ox.flatten()
        res1 = sum([2 ** pos for pos, value in enumerate(ox[::-1]) if value == 1])
        break

for col in range(mat.shape[1]):
    count = np.bincount(co2[:, col])
    least_common = 1 if count[1] < count[0] else 0
    co2 = co2[co2[:, col] == least_common]
    if len(co2) == 1:
        co2 = co2.flatten()
        res2 = sum([2 ** pos for pos, value in enumerate(co2[::-1]) if value == 1])
        break

print(res1 * res2)
