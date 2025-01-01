import time
from typing import Set, Tuple, List
from aoc_utils import  runIt, PuzzleInput, Point, Grid, add, sub
import functools
import math
import re
from itertools import combinations, permutations, product
import sys


testInput = r"""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

testInput2 = r"""T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
.........."""

input = PuzzleInput('input/day8.txt', testInput)

lines = input.getInputLines(test=False)
grid = Grid(lines)

def extend_line(p1:Point, p2:Point) -> List[Point]:
    d = sub(p1, p2)
    
    # generate line out from p1 and p2 until we leave the grid
    def add_gen(p):
        while (p:=add(p, d)) in grid:
            yield p

    def sub_gen(p):
        while (p:=sub(p, d)) in grid:
            yield p

    return [i for i in list(add_gen(p1)) + list(sub_gen(p2))]


def part1():
    antinodes = set()
    for v in grid.unique_values():
        vs = grid.findAll(v)
        for vp in combinations(vs, 2):
            d = sub(*vp)
            antinodes.update(x for x in {add(vp[0], d), sub(vp[1], d)} if x in grid)
    print(f'Count: {len(antinodes)}')

def part2():
    antinodes = set()
    for v in grid.unique_values():
        vs = grid.findAll(v)
        antinodes.update(vs)
        for vp in combinations(vs, 2):
            antinodes.update(extend_line(*vp))
    print(f'Count: {len(antinodes)}')
    # print(grid.to_string({n:'#' for n in antinodes}))

runIt(part1, part2)
