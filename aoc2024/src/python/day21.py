from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  A_star, sliding_window, splitInts, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, groupby, permutations, product
import sys
import numpy


testInput = r"""029A
980A
179A
456A
379A"""

input = PuzzleInput('input/day21.txt', testInput)
lines = input.getInputLines(test=False)

numpad = Grid([['7', '8', '9'],
               ['4', '5', '6'],
               ['1', '2', '3'],
               ['#', '0', 'A']])

dirpad = Grid([['#', '^', 'A'],
               ['<', 'v', '>']])

def dirpad_presses(v1: str, v2: str, grid: Grid) -> list[str]:    
    p1 = grid.find(v1)
    p2 = grid.find(v2)
    diff = sub(p2, p1)

    dx = ''
    dy = ''
    if diff[0] != 0:
        dx = ''.join([('<' if diff[0] < 0 else '>') * abs(diff[0])])
    if diff[1] != 0:
        dy = ''.join([('^' if diff[1] < 0 else 'v') * abs(diff[1])])

    results = set()
    if grid[add(p1, (diff[0], 0))] != '#':
        results.add(dx + dy + 'A')

    if grid[add(p1, (0, diff[1]))] != '#':
        results.add(dy + dx + 'A')

    return list(results)

def press_count(goal: str, level: int, max_level: int) -> int:
    if level == 1:
        return len(goal)
    
    return sum([min_presses_at_level(v1, v2, level, max_level) for (v1, v2) in sliding_window('A' + goal, 2)])
    
@functools.cache
def min_presses_at_level(v1: str, v2: str, level: int, max_level: int) -> int:
    grid = numpad if level == max_level else dirpad
    paths = dirpad_presses(v1, v2, grid)
    total_lens = [press_count(p, level - 1, max_level) for p in paths]
    return min(total_lens)


def part1():
    complexity = 0
    for goal in lines:
        count = press_count(goal, 4, 4)
        print(f'{goal}: {count}')
        complexity += (count * int(goal[:-1]))

    print(f'total complexity: {complexity}')

def part2():
    complexity = 0
    for goal in lines:
        print(f'working on {goal}...')
        count = press_count(goal, 27, 27)
        print(f'{goal}: {count}')
        complexity += (count * int(goal[:-1]))

    print(f'total complexity: {complexity}')

runIt(part1, part2)
