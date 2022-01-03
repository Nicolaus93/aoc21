# -*- coding: utf-8 -*-
import numpy as np

with open("input.txt") as f:
    depths = f.readlines()

arr = np.array([int(i) for i in depths])
print(len(np.where(np.diff(arr) > 0)[0]))

sliding_windows = np.convolve(arr, np.ones(3, dtype=int), "valid")
print(len(np.where(np.diff(sliding_windows) > 0)[0]))
