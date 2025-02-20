from collections import defaultdict
import sys
from aoc_utils import PuzzleInput, add, runIt, Point, manhattan_distance, Grid, cardinal_directions
from itertools import count
from numpy import arctan, arctan2, pi
import math

testInput1 = r"""#########
#b.A.@.a#
#########"""

testInput2 = r"""########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

testInput3 = r"""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""
input = PuzzleInput('input/day18.txt', testInput3)

lines = input.getInputLines(test=True)

def get_reachable_keys(pos: Point, grid: Grid, keys: set[Point], doors: set[Point], steps = 0, visited = set()) -> dict[Point, int]:
    options: dict[Point, int] = dict()
    # print(f'checking for reachable keys from {pos} visited {visited}')
    for d in cardinal_directions:
        new_pos = add(pos, d)
        # print(f'visiting {new_pos} {new_pos in visited} {new_pos in grid} {new_pos in doors} {grid[new_pos]}')
        if new_pos not in visited and new_pos in grid and grid[new_pos] != '#' and new_pos not in doors:
            # print(f'again with {new_pos}')
            visited.add(new_pos)
            if new_pos in keys:
                options[new_pos] = steps + 1
            else:
                options.update(get_reachable_keys(new_pos, grid, keys, doors, steps + 1, visited))
    return options

def explore(pos: Point, grid: Grid, keys: set[Point], doors: set[Point], steps):
    # find the reachable keys, and branch to test all options.
    # when we pick up a key, remove the door for that key.

    options = get_reachable_keys(pos, grid, keys, doors, 0, set())
    print(f'Exploring from {pos} remaining keys {keys} and doors {doors} options: {options}')
    if len(options) == 0: return steps

    best_steps = sys.maxsize
    for k, s in options.items():
        l = grid[k]
        door = l.capitalize()
        print(f'\n\nTrying key {l} with {s} to open {door}')
        new_doors = set()
        new_doors.update(doors)
        door_pos = grid.find(door)
        if door_pos is not None:
            new_doors.remove(door_pos)
        new_keys = set()
        new_keys.update(keys)
        new_keys.remove(k)
        best_steps = min(best_steps, explore(k, grid, new_keys, new_doors, steps + s))

    return best_steps


def part1():
    grid = Grid(lines)
    start = grid.find('@')
    doors = {p for p in grid if grid[p].isupper()}
    keys = {p for p in grid if grid[p].islower()}

    steps = explore(start, grid, keys, doors, 0)
    print(steps)


def part2():
    print('nyi')

runIt(part1, part2)