from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  runIt, PuzzleInput, splitInts, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys


testInput = r"""AAAA
BBCD
BBCC
EEEC"""

testInput2 = r"""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
input = PuzzleInput('input/day12.txt', testInput2)
lines = input.getInputLines(test=False)
grid = Grid(lines)

def build_region(p:Point, visited:Set[Point]) -> Set[Point]:
    if p in visited:
        return set()
    
    visited.add(p)
    region = {p}
    for n in [n for n in grid.neighbors(p, cardinal_directions) if grid[n] == grid[p]]:
        region.update(build_region(n, visited))

    return region

def perimeter(region:Set[Point]) -> int:
    # Count all sides where the neighbor on that side is not also in the region
    return len([add(p, d)
                for p in region
                for d in cardinal_directions
                if add(p,d) not in region])

def sub_sides(points, dir1, dir2, region:Set[Point]) -> int:
    in1 = False
    in2 = False
    count = 0
    for p in points:
        if p not in region:
            in1 = in2  = False
        else:
            if not in1 and add(p, dir1) not in region:
                # starting a new side
                in1 = True
                count += 1
            elif in1 and add(p, dir1) in region:
                # ending a side
                in1 = False

            if not in2 and add(p, dir2) not in region:
                in2 = True
                count += 1
            elif in2 and add(p, dir2) in region:
                in2 = False
    return count

def sides(region:Set[Point]) -> int:
    count = 0

    ys = list(map(lambda p: p[1], region))
    xs = list(map(lambda p: p[0], region))
    xrange = range(min(xs), max(xs) + 1)
    yrange = range(min(ys), max(ys) + 1)

    # look for top and bottom edges by sorting the region into rows
    count += sum([sub_sides([(x, y) for x in xrange], North, South, region) for y in yrange])

    # look for right and left edges by sorting the region into columns
    count += sum([sub_sides([(x, y) for y in yrange], East, West, region) for x in xrange])

    return count

def part1():
    visited = set()

    regions = [r for r in [
        build_region(p, visited) for p in grid
    ] if len(r) > 0]

    price = sum([len(r) * perimeter(r) for r in regions])

    print(f'total price {price}')


def part2():
    visited = set()

    regions = [r for r in [
        build_region(p, visited) for p in grid
    ] if len(r) > 0]

    price = sum([len(r) * sides(r) for r in regions])

    print(f'total price {price}')

runIt(part1, part2)
