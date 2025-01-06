from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  mul, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions_moves, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys
import numpy


testInput = r"""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

testInput2 = r"""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

input = PuzzleInput('input/day15.txt', testInput)
lines = split_on_empty_lines(input.getInputLines(test=False))


def move_robot(pos: Point, move: str, grid: Grid) -> Point:
    # Move until we hit something. If we hit a wall, stop; if we hit a container, recurse.
    next_pos = add(pos, cardinal_directions_moves[move])
    if grid[next_pos] == '#':
        return pos
    elif grid[next_pos] == 'O':
        if (move_robot(next_pos, move, grid) != next_pos):
            grid[next_pos], grid[pos] = grid[pos], grid[next_pos]
            return next_pos
        return pos
    else:
        grid[next_pos], grid[pos] = grid[pos], grid[next_pos]
        return next_pos


def part1():
    grid = Grid(lines[0])
    moves = ''.join(lines[1])
    start = grid.find('@')
    pos = start
    for move in moves:
        pos = move_robot(pos, move, grid)
    gps = sum([100*p[1] + p[0] for p in grid.findAll('O')])
    print(f'gps: {gps}')

def make_wide(s:str) -> str:
    return s.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')

def wide_move(pos: set[Point], dir: Point, grid: Grid):
    # build a set of things to try to move at each step. If they can all move,
    # then backtrack and move them. If any hit a wall, then stop.
    next_moves = set()
    for p in pos:
        next_p = add(p, dir)
        if grid[next_p] == '[':
            next_moves.add(next_p)
            if dir in (North, South):
                next_moves.add(add(next_p, East))
        elif grid[next_p] == ']':
            next_moves.add(next_p)
            if dir in (North, South):
                next_moves.add(add(next_p, West))
        elif grid[next_p] == '#':
            return False

    if len(next_moves) == 0 or wide_move(next_moves, dir, grid):
        for p in pos:
            next_p = add(p, dir)
            grid[p], grid[next_p] = grid[next_p], grid[p]
        return True
    else:
        return False


def part2():
    wide_lines = list(map(make_wide, lines[0]))
    grid = Grid(wide_lines)
    moves = ''.join(lines[1])
    start = grid.find('@')
    pos = start
    for move in moves:
        if (wide_move({pos}, cardinal_directions_moves[move], grid)):
            pos = add(pos, cardinal_directions_moves[move])

    gps = sum([100*p[1] + p[0] for p in grid.findAll('[')])
    print(f'gps: {gps}')
runIt(part1, part2)
