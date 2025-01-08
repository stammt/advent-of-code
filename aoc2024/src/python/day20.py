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

def build_path() -> list[Point]:
    path = [start]
    print(f'start {start}, finish {finish}')
    p = start
    while p != finish:
        neighbors = [n for n in grid.neighbors(p, cardinal_directions) if (grid[n] == '.' or n == finish) and n not in path]
        path.append(neighbors[0])
        p = neighbors[0]

    return path


def find_cheats(steps, threshold = 0):
    path = build_path()

    count = 0
    dist = {p: i for i,p in enumerate(path)}
    for i,p in enumerate(path):
        # find other nodes on path within {threshold} steps of this node
        if i + threshold > len(path): break

        candidates = filter(lambda x: manhattan_distance(p, x) <= steps, path[i+threshold+1:])
        for c in candidates:
            savings = dist[c] - dist[p] - manhattan_distance(p, c)
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
