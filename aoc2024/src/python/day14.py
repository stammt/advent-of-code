from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  mul, runIt, PuzzleInput, split_on_empty_lines, splitInts, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys
import numpy


testInput = r"""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

input = PuzzleInput('input/day14.txt', testInput)
lines = input.getInputLines(test=False)

# parse into initial position, vector
def parse_robot(line:str) -> tuple:
    parts = line.split(' ')
    pos = splitInts(parts[0][2:], ',')
    vec = splitInts(parts[1][2:], ',')
    return (pos, vec)

def move(p: Point, steps: Point, size: Point) -> Point:
    x = (p[0] + steps[0]) % size[0]
    # if x >= size[0]:
    #     x = x % size[0]
    # elif x < 0:
    #     x = abs(x % size[0])
    y = (p[1] + steps[1]) % size[1]
    # if y >= size[1]:
    #     y = y % size[1]
    # elif y < 0:
    #     y = abs(y % size[1])
    return (x, y)

def part1():
    robots = list(map(parse_robot, lines))
    size = (101, 103) # (11, 7)
    grid = defaultdict(int)

    for bot in robots:
        p = move(bot[0], mul(bot[1], 100), size)
        grid[p] = grid[p] + 1
    
    q1 = sum(grid[x, y] for x in range(size[0] // 2) for y in range(size[1] // 2))
    q2 = sum(grid[x, y] for x in range((size[0] // 2) + 1, size[0]) for y in range(size[1] // 2))
    q3 = sum(grid[x, y] for x in range(size[0] // 2) for y in range((size[1] // 2) + 1, size[1]))
    q4 = sum(grid[x, y] for x in range((size[0] // 2) + 1, size[0]) for y in range((size[1] // 2) + 1, size[1]))

    print(f'safety factor {q1 * q2 * q3 * q4} ({q1} {q2} {q3} {q4})')

# look for a contiguous block of robots
def find_block(start:Point, grid) -> bool:
    if start not in grid: return False
    return all([(x, y) in grid for x in range(start[0], start[0] + 15) for y in range(start[1], start[1] + 3)])

def part2():
    robots = list(map(parse_robot, lines))
    size = (101, 103) # (11, 7)

    # dict of position -> list of step
    grid = defaultdict(list)
    for bot in robots:
        grid[bot[0]].append(bot[1])


    for s in range(7000):
        ng = defaultdict(list)
        for (p, steps) in grid.items():
            for step in steps:
                np = move(p, step, size)
                ng[np].append(step)
        grid = ng

        # find a line of len 10?
        for y in range(size[1]):
            for x in range(size[0]):
                if find_block((x, y), grid):
                    points = {}
                    for i in range(size[0]):
                        for j in range(size[1]):
                            points[(i,j)] = '#' if (i,j) in grid else '.'
                    tree = Grid(points)
                    print(tree)
                    print(f'tree? {s+1}')
                    return


    print(f'nyi')

runIt(part1, part2)
