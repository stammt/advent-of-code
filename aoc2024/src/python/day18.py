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

    grid = Grid([['.' for x in range(grid_size)] for y in range(grid_size)])
    for i in range(falling):
        grid[splitInts(lines[i], ',')] = CORRUPTED

    start = (0,0)
    finish = (grid_size-1, grid_size-1)
    path = set(A_star(start, finish, lambda p: manhattan_distance(p, finish), grid))

    # Drop bytes until we no longer get a path from A_star. Only recalculate the path if the
    # byte would block our previous shortest path.
    # Note - this would be more efficient to calculate ALL paths and only recalculate if any of 
    # them get blocked...
    for i in range(falling, len(lines)):
        next_byte = splitInts(lines[i], ',')
        grid[next_byte] = CORRUPTED
        if next_byte in path:
            path = set(A_star(start, finish, lambda p: manhattan_distance(p, finish), grid))
            if len(path) == 0:
                print(f'No more path after {next_byte}')
                break

    print(f'Done part 2')


    
runIt(part1, part2)
