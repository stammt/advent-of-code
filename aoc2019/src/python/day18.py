from collections import defaultdict
from functools import cache
from heapq import heappop, heappush
import sys
from aoc_utils import PuzzleInput, add, reconstruct_path, runIt, Point, manhattan_distance, Grid, cardinal_directions
from itertools import count, permutations
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
input = PuzzleInput('input/day18.txt', testInput4)

lines = input.getInputLines(test=False)

ORD_A = ord('a')

def is_locked(door: str, have_keys: int) -> bool:
    key_index = ord(door.lower()) - ORD_A
    return have_keys & (1 << key_index) == 0

def add_key(key: str, have_keys: int) -> int:
    key_index = ord(key) - ORD_A
    return have_keys | (1 << key_index)

def count_missing_keys(have_keys: int, all_keys: int) -> int:
    count = 0
    while (have_keys):
        count += (have_keys & 1)
        have_keys >>= 1
    return all_keys - count

def solve_astar(start_pos: Point, grid: Grid):
    all_keys_pos = {p for p in grid if grid[p].islower()}
    all_keys = 0
    key_count = len(all_keys_pos)
    for i in range(len(all_keys_pos)):
        all_keys |= (1 << i)

    # nodes are (x, y, <bitmask of collected keys>)
    start = (start_pos[0], start_pos[1], 0)

    openSet = []
    heappush(openSet,(key_count, start))

    cameFrom: dict[tuple[int, int, int], Point] = dict()

    # For node n, gScore[n] is the currently known cost of the cheapest path from start to n.
    gScore: dict[tuple[int, int, int], int]  = defaultdict(lambda: sys.maxsize)
    gScore[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore: dict[tuple[int, int, int], int] = defaultdict(lambda: sys.maxsize)
    fScore[start] = key_count

    while len(openSet) > 0:
        (priority, current) = heappop(openSet) # min([n for n in openSet if n in fScore], key=lambda x: fScore[x])
        have_keys = current[2]
        if have_keys == all_keys:
            return gScore[current]
        
        for n_pos in [add((current[0], current[1]), d) for d in cardinal_directions if add((current[0], current[1]), d) in grid and grid[add((current[0], current[1]), d)] != '#']:
            if grid[n_pos].isupper() and is_locked(grid[n_pos], have_keys): continue
            
            n_keys = have_keys
            if (grid[n_pos].islower()):
                n_keys = add_key(grid[n_pos], have_keys)            
            n = (n_pos[0], n_pos[1], n_keys)
            tentative_gScore = gScore[current] + 1 # distance is always 1 here
            if tentative_gScore < gScore[n]:
                cameFrom[n] = current
                gScore[n] = tentative_gScore
                fScore[n] = tentative_gScore + count_missing_keys(n_keys, key_count) # 'h' function, use the number of keys still to retrieve
                if n not in openSet:
                    heappush(openSet, (fScore[n], n))

    return []    


def part1():
    original_grid = Grid(lines)
    start = original_grid.find('@')
    result = solve_astar(start, original_grid)

    # 6286
    print(result)


def part2():
    print('nyi')

runIt(part1, part2)
