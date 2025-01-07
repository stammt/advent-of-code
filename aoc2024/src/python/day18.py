from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  A_star, manhattan_distance, splitInts, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys
import numpy


testInput = r"""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


CORRUPTED = '#'

input = PuzzleInput('input/day18.txt', testInput)
lines = input.getInputLines(test=False)



def part1():
    grid_size = 71
    falling = 1024

    grid = Grid([['.' for x in range(grid_size)] for y in range(grid_size)])
    for i in range(falling):
        grid[splitInts(lines[i], ',')] = CORRUPTED

    start = (0,0)
    finish = (grid_size-1, grid_size-1)
    path = A_star(start, finish, lambda p: manhattan_distance(p, finish), grid)
    # len(path) is the number of nodes in the path, number of steps is len - 1
    print(f'min steps: {len(path) - 1}')


def part2():
    grid_size = 71
    falling = 1024

    base_grid = Grid([['.' for x in range(grid_size)] for y in range(grid_size)])

    start = (0,0)
    finish = (grid_size-1, grid_size-1)

    # we know up to 1024 is ok, so do a binary search from 1024 to the end to find where it's blocked
    good = falling + 1
    bad = len(lines)
    while bad != (good + 1):
        mid = (good + bad) // 2
        
        grid = Grid(base_grid)
        for i in range(mid):
            grid[splitInts(lines[i], ',')] = CORRUPTED

        path = set(A_star(start, finish, lambda p: manhattan_distance(p, finish), grid))
        if len(path) == 0:
            bad = mid
        else:
            good = mid
        
    print(f'No more path after {lines[bad-1]}')


    
runIt(part1, part2)
