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

# 8
testInput5 = r"""#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######"""

# 32
testInput6 = r"""#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############"""

# 72
testInput7 = r"""#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""

input = PuzzleInput('input/day18.txt', testInput7)

lines = input.getInputLines(test=False)

ORD_A = ord('a')

def is_locked(door: str, have_keys: int) -> bool:
    key_index = ord(door.lower()) - ORD_A
    return have_keys & (1 << key_index) == 0

def add_key(key: str, have_keys: int) -> int:
    key_index = ord(key) - ORD_A
    return have_keys | (1 << key_index)

def has_key(key: str, have_keys: int) -> int:
    key_index = ord(key) - ORD_A
    return have_keys & (1 << key_index) != 0

def count_missing_keys(have_keys: int, all_keys: int) -> int:
    count = 0
    while (have_keys):
        count += (have_keys & 1)
        have_keys >>= 1
    return all_keys - count

# Find the keys that are reachable and have not been collected yet.
# This assumes there is only one path to each reachable key which is true in the input data!
def find_next_keys(pos: Point, have_keys: int, grid: Grid) -> list[tuple[Point, int]]: # Key position and number of steps
    results = []
    q = [(pos, 0)]
    visited = {pos}
    while q:
        p = q.pop()
        visited.add(p[0])
        if grid[p[0]].islower() and not has_key(grid[p[0]], have_keys):
            results.append(p)
        else:
            for n in grid.neighbors(p[0], cardinal_directions):
                if n in visited: continue
                if grid[n] == '#': continue
                if grid[n].isupper() and is_locked(grid[n], have_keys): continue
                q.append((n, p[1] + 1))
    return results

# treat the grid as a graph of nodes (x, y, <keys>) and find the shortest path that brings us to a node with all keys collected
def solve_part1_astar(start_pos: Point, grid: Grid):
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
        (priority, current) = heappop(openSet)
        have_keys = current[2]
        if have_keys == all_keys:
            return gScore[current]
        
        for next_key in find_next_keys((current[0], current[1]), have_keys, grid):
            n_pos = next_key[0]
            if grid[n_pos].isupper() and is_locked(grid[n_pos], have_keys): continue
            
            n_keys = have_keys
            if (grid[n_pos].islower()):
                n_keys = add_key(grid[n_pos], have_keys)            
            n = (n_pos[0], n_pos[1], n_keys)
            tentative_gScore = gScore[current] + next_key[1]
            if tentative_gScore < gScore[n]:
                cameFrom[n] = current
                gScore[n] = tentative_gScore
                fScore[n] = tentative_gScore + count_missing_keys(n_keys, key_count) # 'h' function, use the number of keys still to retrieve
                if n not in openSet:
                    heappush(openSet, (fScore[n], n))

    return []


# Similar to solving part1, but each node has 4 positions in addition to the collected keys.
def solve_part2_astar(start_pos: list[Point], grid: Grid):
    all_keys_pos = {p for p in grid if grid[p].islower()}
    all_keys = 0
    key_count = len(all_keys_pos)
    for i in range(len(all_keys_pos)):
        all_keys |= (1 << i)

    # nodes are (p0, p1, p2, p3, <bitmask of collected keys>)
    start = (start_pos[0], start_pos[1], start_pos[2], start_pos[3], 0)

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
        (priority, current) = heappop(openSet)
        have_keys = current[4]
        if have_keys == all_keys:
            return gScore[current]
        
        # Move the bots one at a time, treating any reachable keys as neighbors. Moving one block at a time
        # is too slow and creates too many combinations between the robot's positions.
        for bot in range(4):
            for next_key in find_next_keys(current[bot], have_keys, grid):
                n_pos = next_key[0]
                if grid[n_pos].isupper() and is_locked(grid[n_pos], have_keys): continue
                
                n_keys = have_keys
                if (grid[n_pos].islower()):
                    n_keys = add_key(grid[n_pos], have_keys)

                # Update the current tuple with the moved bot
                n_list = [p for p in current]
                n_list[bot] = n_pos
                n_list[4] = n_keys
                n = tuple(n_list)
                tentative_gScore = gScore[current] + next_key[1]
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
    result = solve_part1_astar(start, original_grid)

    # 6286
    print(result)


def part2():
    original_grid = Grid(lines)
    center = original_grid.find('@')
    starts = [add(center, (-1, -1)), add(center, (1, 1)), add(center, (-1, 1)), add(center, (1, -1))]
    original_grid[add(center, (1, 0))] = '#'
    original_grid[add(center, (-1, 0))] = '#'
    original_grid[add(center, (0, 1))] = '#'
    original_grid[add(center, (0, -1))] = '#'
    original_grid[center] = '#'

    result = solve_part2_astar(starts, original_grid)

    # result = 2140
    print(result)

runIt(part1, part2)
