from operator import add, mul
import time
from typing import Set
from aoc_utils import North, runIt, PuzzleInput, Grid, Point, add, turn, x, y
import functools
import math
import re
from itertools import combinations
import sys


testInput = r"""....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#..."""

input = PuzzleInput('input/day6.txt', testInput)

lines = input.getInputLines(test=False)
grid = Grid(lines)
start = grid.find('^')

def findVisited() -> Set[Point]:
    dir = North
    path = [start]
    while (grid.isInRange(nextPos := add(path[-1], dir))):
        if (grid.get(nextPos) == '#'):
            dir = turn(dir, 'R')
        else:
            path.append(nextPos)

    return set(path)

def causesLoop(obstacle: Point) -> bool:
    dir = North
    pos = start
    turns = {(start, dir)}
    while (grid.isInRange(nextPos := add(pos, dir))):
        if (grid.get(nextPos) == '#'):
            dir = turn(dir, 'R')
            if ((nextPos, dir) in turns):
                return True
            turns.add((nextPos, dir))
        else:
            pos= nextPos
    return False

def part1():
    visited = findVisited()
    print(f'visited {len(visited)}')

def part2():
    baseVisited = findVisited()
    c = 0
    for p in baseVisited - {start}:
        grid.lines[p[1]][p[0]] = '#'
        if (causesLoop(p)):
            c+=1
        grid.lines[p[1]][p[0]] = '.'

    print(f'sum: {c}')

runIt(part1, part2)