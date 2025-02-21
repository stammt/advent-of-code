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
input = PuzzleInput('input/day18.txt', testInput4)

lines = input.getInputLines(test=False)

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

def add_distances_to_keys(k_pos, distances, blocking_doors, grid):
    key = grid[k_pos]

    visited = set()
    visited.add(k_pos)

    q = [(k_pos, 0, set())] # position, steps, doors encountered
    while q:
        state = q.pop()
        for d in cardinal_directions:
            new_pos = add(state[0], d)
            if new_pos not in visited and new_pos in grid and grid[new_pos] != '#':
                visited.add(new_pos)
                if grid[new_pos].islower():
                    other_key = grid[new_pos]
                    print(f'looking at {key} to {other_key}')
                    if (key, other_key) not in distances or distances(key, other_key) > state[1] + 1:
                        distances[(key, other_key)] = state[1] + 1
                        blocking_doors[(key, other_key)] = state[2]
                    else:
                        print(f'already found distance for {key}, {other_key}')

                new_doors = set()
                new_doors.update(state[2])
                if grid[new_pos].isupper():
                    new_doors.add(grid[new_pos])
                q.append((new_pos, state[1] + 1, new_doors))

def part1():
    original_grid = Grid(lines)
    start = original_grid.find('@')
    all_keys = {p for p in original_grid if original_grid[p].islower()}
    all_key_names = {original_grid[p] for p in all_keys}
    print(all_key_names)

    doors = {original_grid[p] for p in original_grid if original_grid[p].isupper()}
    print(doors)
    print(len(doors))

    # build a dictionary of the steps between all pairs of keys
    # key is a pair of keys, value is number of steps e.g. distances[(a,b)] = 7
    key_distances = dict()
    # dictionary of the doors between the keys 
    blocking_doors = dict()

    for k in all_keys:
        add_distances_to_keys(k, key_distances, blocking_doors, original_grid)

    # Add the distances from start to all of the keys
    add_distances_to_keys(start, key_distances, blocking_doors, original_grid)

    start_state = (start, 0, set()) # position, steps, keys
    q = [start_state]

    best = sys.maxsize
    while q:
        state = q.pop(0)

        pos = state[0]
        steps = state[1]
        keys = state[2]
        if keys == all_key_names:
            if steps < best:
                print(f'Have all keys: {steps}')
                best = min(best, steps)
            continue

        if steps > best:
            # print(f'Cutting off at {steps}')
            continue

        open_doors = set(map(lambda s: s.capitalize(), keys))
        last_key = original_grid[pos]

        next_states = []
        for pair in key_distances.keys():
            # not from this key
            if pair[0] != last_key: continue
            # to a key we already have
            if pair[1] in keys: continue
            # is still blocked by a door
            if not open_doors.issuperset(blocking_doors[pair]): continue

            # print(f'Queuing {pair} {key_distances[pair]}')
            next_pos = original_grid.find(pair[1])
            next_keys = set()
            next_keys.update(keys)
            next_keys.add(pair[1])
            next_states.append((next_pos, steps + key_distances[pair], next_keys))
        next_states.sort(key = lambda s: s[1], reverse=True)
        for s in next_states:
            q.insert(0, s)

    # 7410 too high
    print(best)



def part2():
    print('nyi')

runIt(part1, part2)