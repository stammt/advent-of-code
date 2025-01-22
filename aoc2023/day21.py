from aoc_utils import runIt, PuzzleInput, Grid, Point
import functools
import math
import re
import itertools
import sys

testInput = r"""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
input = PuzzleInput('input-day21.txt', testInput)
lines = input.getInputLines(test=False)

def part1():
    grid = Grid(lines)
    start = grid.find('S')
    grid[start] = '.'

    stepGoal = 64
    q = {start}

    for i in range(stepGoal):
        stepq = list(q)
        q = set()
        while len(stepq) > 0:
            step = stepq.pop()
            q.update(n for n in grid.neighbors(step) if grid[n] == '.')
    
    # plots = set(q)
    # overlay = {p:'O' for p in plots}
    # print(grid.to_string(overlay))

    print(f'Hit {len(q)}')


def part2():
    total = 0
    print(f'Hit {total}')

runIt(part1, part2)
