from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  A_star, manhattan_distance, splitInts, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, groupby, permutations, product
import sys
import numpy


testInput = r"""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

input = PuzzleInput('input/day20.txt', testInput)
lines = input.getInputLines(test=False)
grid = Grid(lines)
start = grid.find('S')
finish = grid.find('E')

def build_path() -> dict[Point, int]:
    path = {start: 0}
    print(f'start {start}, finish {finish}')
    p = start
    steps = 0
    while p != finish:
        neighbors = [n for n in grid.neighbors(p, cardinal_directions) if (grid[n] == '.' or n == finish) and n not in path]
        p = neighbors[0]
        steps += 1
        path[p] = steps

    return path


def find_cheats(steps, threshold = 0):
    dist = build_path()

    count = 0
    for p in dist.keys():
        # find other nodes on path within {threshold} steps of this node
        for x in range(p[0]-steps, p[0]+steps+1):
            for y in range(p[1]-steps, p[1]+steps+1):
                if (x,y) in dist:
                    md = manhattan_distance(p, (x,y))
                    if md <= steps:
                        savings = dist[(x,y)] - dist[p] - md
                        if (savings >= threshold):
                            count += 1                        
    return count

def part1():
    cheats = find_cheats(2, 100)
    print(f'cheats > 100: {cheats}')
    

def part2():
    cheats = find_cheats(20, 100)
    print(f'cheats > 100: {cheats}')


runIt(part1, part2)
