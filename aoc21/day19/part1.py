# -*- coding: utf-8 -*-
import time
from collections import Counter, defaultdict
from itertools import combinations, product

import numpy as np
import torch
from aocd.models import Puzzle
from optimal_pytorch.coin_betting.torch import Cocob
from scipy.spatial.distance import pdist, squareform

TOT_ITER = 0


def loss_f(x1, x2, model):
    return torch.linalg.norm(x1 - x2 @ model, axis=1).sum() / len(x1)


def optimize(cloud_1, cloud_2):
    global TOT_ITER

    centered_cloud_1 = cloud_1 - cloud_1.mean(axis=0)
    centered_cloud_2 = cloud_2 - cloud_2.mean(axis=0)
    centered_cloud_1 = torch.tensor(centered_cloud_1).float()
    centered_cloud_2 = torch.tensor(centered_cloud_2).float()
    model = torch.eye(3, requires_grad=True)
    # optimizer = torch.optim.SGD([model], lr=1e-4)
    optimizer = Cocob([model])
    iterations = 10000
    cum_loss = 0
    for step in range(iterations):
        optimizer.zero_grad()
        loss = loss_f(centered_cloud_1, centered_cloud_2, model)
        loss.backward()
        optimizer.step()
        cum_loss += loss.item()
        converged = torch.all(
            torch.isclose(
                centered_cloud_1, centered_cloud_2 @ torch.round(model.detach())
            )
        )
        if converged:
            break

    TOT_ITER += step
    if not converged:
        raise ValueError(
            f"Method has not converged!\n"
            f"Rotation matrix:\n"
            f"{torch.round(model.detach())}\n"
            f"Loss at step {step}: {loss.item()}"
        )
    rot_mat = np.rint(model.detach().numpy()).astype(int)
    transl_vec = cloud_1[0] - cloud_2[0] @ rot_mat
    return rot_mat, transl_vec


def solve(point_clouds):
    global TOT_ITER
    start = time.time()
    couples = []
    for cloud_1, cloud_2 in combinations(range(len(point_clouds)), 2):
        dist_1 = pdist(point_clouds[cloud_1])
        dist_2 = pdist(point_clouds[cloud_2])
        shared_distances = set(dist_1) & set(dist_2)
        if len(shared_distances) >= 66:
            couples.append((cloud_1, cloud_2))
            couples.append((cloud_2, cloud_1))

    path = []
    vis = set()
    get_right_path(couples, path, vis)
    transl_vectors = []
    for couple in path:
        first, second = couple
        rot_mat, transl_vec = find_affine_transf(
            point_clouds[first], point_clouds[second]
        )
        point_clouds[second] = point_clouds[second] @ rot_mat + transl_vec
        transl_vectors.append(transl_vec)

    common_points = set()
    for cloud in point_clouds:
        for point in cloud:
            common_points.add(tuple(point))

    max_dist = max(pdist(transl_vectors, "cityblock"))
    print(f"part1: {len(common_points)}")
    print(f"part2: {int(max_dist)}")
    print(f"time: {time.time() - start:.3f}")
    print(f"iterations: {TOT_ITER}")
    print()
    TOT_ITER = 0


def find_affine_transf(points_1, points_2):
    pairwise_dist_1 = pdist(points_1, "sqeuclidean")
    pairwise_dist_2 = pdist(points_2, "sqeuclidean")
    shared_distances = set(pairwise_dist_1) & set(pairwise_dist_2)
    if len(shared_distances) < 66:
        raise ValueError("At least 12 points are required!")
    dist_1 = squareform(pairwise_dist_1)
    dist_1[np.tril_indices(len(dist_1))] = 0
    dist_2 = squareform(pairwise_dist_2)
    dist_2[np.tril_indices(len(dist_2))] = 0
    graph_dict = defaultdict(Counter)
    for dist in shared_distances:
        first_group = np.where(dist == dist_1)
        second_group = np.where(dist == dist_2)

        for node1 in first_group:
            for node2 in second_group:
                try:
                    graph_dict[node1.item()][node2.item()] += 1
                except ValueError:
                    for couple in product(node1, node2):
                        graph_dict[couple[0]][couple[1]] += 1
    graph_dict = {
        node: graph_dict[node].most_common(1)[0][0]
        for node in graph_dict.keys()
        if graph_dict[node].most_common(1)[0][1] >= 11
    }

    # retrieve affine transformation
    first = points_1[list(graph_dict.keys())]
    second = points_2[list(graph_dict.values())]
    rot_mat, transl_vec = optimize(first, second)
    return rot_mat, transl_vec


def get_right_path(relations, path, visited, couple=(-1, 0)):
    couples = [i for i in relations if i[0] == couple[1]]
    for new_couple in couples:
        if new_couple[1] not in visited and new_couple != couple[::-1]:
            path.append(new_couple)
            visited.add(new_couple[1])
            # recursively find next scanners
            get_right_path(relations, path, visited, couple=new_couple)


if __name__ == "__main__":
    # test_puzzle
    scanners = list()
    with open("test.txt") as f:
        for line in f:
            if "scanner" in line:
                scanners.append(list())
            elif len(line.strip()) == 0:
                scanners[-1] = np.array(scanners[-1])
            else:
                scanners[-1].append(tuple(int(i) for i in line.strip().split(",")))
    scanners[-1] = np.array(scanners[-1])
    solve(scanners)

    # real puzzle
    scanners = []
    puzzle = Puzzle(year=2021, day=19)
    for line in puzzle.input_data.split("\n"):
        if "scanner" in line:
            scanners.append(list())
        elif len(line.strip()) == 0:
            scanners[-1] = np.array(scanners[-1])
        else:
            scanners[-1].append(tuple(int(i) for i in line.strip().split(",")))
    scanners[-1] = np.array(scanners[-1])
    solve(scanners)
