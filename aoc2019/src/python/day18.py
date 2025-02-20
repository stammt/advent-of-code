from collections import defaultdict
from functools import cache
import sys
from aoc_utils import PuzzleInput, add, runIt, Point, manhattan_distance, Grid, cardinal_directions
from itertools import count
from numpy import arctan, arctan2, pi
import math

# 8
testInput1 = r"""#########
#b.A.@.a#
#########"""

# 86
testInput2 = r"""########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

# 136
testInput3 = r"""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

# 81
testInput4 = r"""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""
input = PuzzleInput('input/day18.txt', testInput3)

lines = input.getInputLines(test=True)

reachable_cache = dict()
def get_reachable_keys(pos: Point, grid: Grid) -> dict[Point, int]:
    global reachable_cache

    keys = frozenset([p for p in grid if grid[p].islower()])
    doors = frozenset([p for p in grid if grid[p].isupper()])
    cache_key = (pos, keys, doors)
    if cache_key in reachable_cache:
        # print(f'Cache hit {cache_key}')
        return reachable_cache[cache_key]
    
    options: dict[Point, int] = dict()
    q = [(pos, 0)]
    # print(f'checking for reachable keys from {pos} steps {steps} visited {visited}')
    visited = set()
    visited.add(pos)

    while q:
        state = q.pop(0)
        for d in cardinal_directions:
            new_pos = add(state[0], d)
            # print(f'visiting {new_pos} {new_pos in visited} {new_pos in grid} {grid[new_pos]}')
            if new_pos not in visited and new_pos in grid and grid[new_pos] != '#' and not grid[new_pos].isupper():
                # print(f'again with {new_pos}')
                visited.add(new_pos)
                if grid[new_pos].islower() and (new_pos not in options or options[new_pos] > state[1]):
                    options[new_pos] = state[1] + 1
                else:
                    q.append((new_pos, state[1] + 1))
                    # options.update(get_reachable_keys(new_pos, grid, steps + 1, visited))

    reachable_cache[cache_key] = options
    return options

def part1():
    original_grid = Grid(lines)
    start = original_grid.find('@')

    q = [(original_grid, start, 0, [])] # grid, position, steps, keys

    best = sys.maxsize
    best_state = None
    while q:
        state = q.pop(0)
        if state[2] > best:
            print(f'Nope on {state[2]}')
            continue

        options = get_reachable_keys(state[1], state[0])

        if len(options) == 0:
            print(f'0 options with {state[1]} {state[2]} {state[3]}\n')
            # best = min(best, state[2])
            if state[2] < best:
                best = state[2]
                best_state = state
        else:
            # print(f'{len(options)} options with {state[1]} {state[2]}')
            for key_pos, steps in options.items():
                state_grid = state[0]
                key = state_grid[key_pos]
                door = key.capitalize()
                door_pos = state_grid.find(door)

                grid_copy = Grid(state_grid)
                grid_copy[key_pos] = '.'
                if door_pos != None:
                    # print(f'Removing door {door} at {door_pos}')
                    grid_copy[door_pos] = '.'

                # print(f'Taking key {key} for {steps} already {state[2]} {state[3]}')
                total_steps = state[2] + steps
                total_keys = state[3] + [key]

                if total_steps < best:
                    q.append((grid_copy, key_pos, total_steps, total_keys))
                # else:
                #     print(f'Cutting off with {total_steps}')


    print(best)
    print(best_state[3])


def part2():
    print('nyi')

runIt(part1, part2)