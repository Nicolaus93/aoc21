# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import typing
from dataclasses import dataclass
from itertools import product

from aocd.models import Puzzle
from tqdm import tqdm


@dataclass(frozen=True)
class Cuboid:
    x_range: tuple
    y_range: tuple
    z_range: tuple

    def volume(self) -> int:
        x_len = self.x_range[1] - self.x_range[0]
        y_len = self.y_range[1] - self.y_range[0]
        z_len = self.z_range[1] - self.z_range[0]
        return x_len * y_len * z_len

    def intersection(self, other: Cuboid) -> typing.Optional[Cuboid]:
        x_intersection = Cuboid.range_intersection(self.x_range, other.x_range)
        y_intersection = Cuboid.range_intersection(self.y_range, other.y_range)
        z_intersection = Cuboid.range_intersection(self.z_range, other.z_range)
        if x_intersection and y_intersection and z_intersection:
            return Cuboid(x_intersection, y_intersection, z_intersection)
        return None

    def split(self, other: Cuboid) -> typing.Tuple[typing.Set[Cuboid], Cuboid]:
        splitting = set()
        intersecting_cuboid = self.intersection(other)
        if intersecting_cuboid:
            x_ranges = Cuboid.get_ranges(
                [x for cuboid in (other, intersecting_cuboid) for x in cuboid.x_range]
            )
            y_ranges = Cuboid.get_ranges(
                [y for cuboid in (other, intersecting_cuboid) for y in cuboid.y_range]
            )
            z_ranges = Cuboid.get_ranges(
                [z for cuboid in (other, intersecting_cuboid) for z in cuboid.z_range]
            )
            for xs, ys, zs in product(x_ranges, y_ranges, z_ranges):
                new_cuboid = Cuboid(xs, ys, zs)
                if new_cuboid != intersecting_cuboid:
                    splitting.add(new_cuboid)
        return splitting, intersecting_cuboid

    @staticmethod
    def get_ranges(cuboids_ranges):
        all_coord = sorted(set(cuboids_ranges))
        return [tuple((i, j)) for i, j in zip(all_coord, all_coord[1:])]

    @staticmethod
    def range_intersection(range_1, range_2):
        min1, max1 = range_1
        min2, max2 = range_2
        if min1 <= min2 < max1:
            if max2 < max1:
                return min2, max2
            else:
                return min2, max1
        if min2 <= min1 < max2:
            if max1 < max2:
                return min1, max1
            else:
                return min1, max2
        return None

    def subtract(
        self, others: typing.Union[typing.Set[Cuboid], Cuboid], debug: bool = False
    ) -> typing.Set[Cuboid]:
        solid = {self}
        if not isinstance(others, set):
            others = {others}

        def measure_volume(x):
            return sum(c.volume() for c in x)

        original_volume = measure_volume(solid) - measure_volume(others)

        while others:
            if debug:
                new_volume = measure_volume(solid) - measure_volume(others)
                if new_volume != original_volume:
                    raise ValueError(
                        f"Original volume = {original_volume}, new volume = {new_volume}!"
                    )

            other = others.pop()
            to_remove = set()
            to_add = set()
            for cuboid in solid:
                new_split, intersect = other.split(cuboid)
                if intersect:
                    to_remove.add(cuboid)
                    to_add |= new_split
            solid -= to_remove
            solid |= to_add

        return solid


def test():
    c1 = Cuboid((0, 3), (0, 3), (0, 3))
    c2 = Cuboid((1, 2), (1, 2), (1, 2))
    c3 = c1.intersection(c2)
    new_cs, intersect_c = Cuboid.split(c1, c2)
    print(c3, new_cs, intersect_c)

    c1 = Cuboid((1, 3), (2, 4), (5, 7))
    c2 = Cuboid((2, 4), (1, 3), (5, 7))
    c3 = c1.intersection(c2)
    new_cs, intersect_c = Cuboid.split(c1, c2)
    print(c3, new_cs, intersect_c)


def gen_cuboid(str_coords: str) -> Cuboid:
    coords = list(map(int, re.findall(r"-?\d+", str_coords)))
    x0, x1 = coords[0], coords[1] + 1
    y0, y1 = coords[2], coords[3] + 1
    z0, z1 = coords[4], coords[5] + 1
    return Cuboid((x0, x1), (y0, y1), (z0, z1))


def solve(
    instructions: typing.List[typing.Tuple[str, Cuboid]], debug: bool = False
) -> typing.Set[Cuboid]:
    final_solid = set()
    for command, new_cub in tqdm(instructions):
        to_remove = set()
        to_add = set()
        if command == "on":
            final_solid.add(new_cub)
            all_intersections = set()
            # check for intersection
            for old_cub in final_solid:
                if old_cub != new_cub and old_cub.intersection(new_cub):
                    old_splits, intersect = new_cub.split(old_cub)
                    all_intersections.add(intersect)
                    to_remove.add(old_cub)
                    to_remove.add(new_cub)
                    to_add |= old_splits | {intersect}  # add new cuboids
            new_splits = new_cub.subtract(all_intersections)
            final_solid = final_solid - to_remove | to_add | new_splits
        elif command == "off":
            for old_cub in final_solid:
                intersect = old_cub.intersection(new_cub)
                if intersect:
                    new_splits = old_cub.subtract(intersect)
                    to_remove.add(old_cub)
                    to_add |= new_splits
            final_solid = final_solid - to_remove | to_add
        else:
            raise ValueError(f"Wrong command: {command}!")
        if debug:
            print(f"volume: {sum(c.volume() for c in final_solid)}")
    return final_solid


if __name__ == "__main__":
    # test_puzzle
    input_instructions = list()
    with open("test.txt") as f:
        for line in f:
            instr, ranges = line.strip().split()
            cub = gen_cuboid(ranges)
            input_instructions.append((instr, cub))

    final_cuboids = solve(input_instructions)
    print(f"test: {sum(c.volume() for c in final_cuboids)}")

    # real puzzle
    input_instructions = list()
    puzzle = Puzzle(year=2021, day=22)
    for line in puzzle.input_data.split("\n"):
        instr, ranges = line.strip().split()
        cub = gen_cuboid(ranges)
        input_instructions.append((instr, cub))

    final_cuboids = solve(input_instructions)
    print(f"part2: {sum(c.volume() for c in final_cuboids)}")
