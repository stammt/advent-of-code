from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  runIt, PuzzleInput, Point, Grid, add, sub, cardinal_directions
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys


testInput = r"""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

testInput2 = r"""12345"""

input = PuzzleInput('input/day10.txt', testInput)

lines = input.getInputLines(test=False, mapper=int)
grid = Grid(lines)

# For each trailhead, spread out on any path that increases by one level, and then repeat.
# Use a set to get only the unique end points.
def part1():
    trailheads = grid.findAll(0)
    total = 0
    for th in trailheads:
        steps = {th}
        level = 0
        while level < 9 and len(steps) > 0:
            neighbors = [grid.neighbors(p, cardinal_directions) for p in steps]
            steps = set(filter(lambda x: grid[x] == level + 1, chain.from_iterable(neighbors)))
            level += 1
        total += len(steps)

    print(f'total score {total}')


# Same as part 1 but with a list to get all paths instead of unique endings
def part2():
    trailheads = grid.findAll(0)
    total = 0
    for th in trailheads:
        steps = [th]
        level = 0
        while level < 9 and len(steps) > 0:
            neighbors = [grid.neighbors(p, cardinal_directions) for p in steps]
            steps = list(filter(lambda x: grid[x] == level + 1, chain.from_iterable(neighbors)))
            level += 1
        total += len(steps)

    print(f'total score {total}')

runIt(part1, part2)
