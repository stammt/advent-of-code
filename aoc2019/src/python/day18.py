from collections import defaultdict
from functools import cache
import sys
from aoc_utils import PuzzleInput, add, runIt, Point, manhattan_distance, Grid, cardinal_directions
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

lines = input.getInputLines(test=True)

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



best_so_far = sys.maxsize

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

    def solve(path, remaining, steps):
        global best_so_far
        if steps > best_so_far:
            return sys.maxsize
        
        if len(remaining) == 0:
            best_so_far = min(best_so_far, steps)
            return steps
        
        print(f'{path} : {remaining}')
        last_key = '@' if len(path) == 0 else path[-1]

        path_set = set(map(lambda k: k.capitalize(), path))
        best = sys.maxsize 
        for i in range(len(remaining)):
            key = remaining[i]
            doors = blocking_doors[last_key, key]
            if path_set.issuperset(doors):
                next_path = path + [key]
                best = min(best, solve(next_path, remaining[0:i] + remaining[i+1:], steps + key_distances[last_key, key]))

        return best

    result = solve([], list(all_key_names), 0)

    # 7010 too high
    print(result)



def part2():
    print('nyi')

runIt(part1, part2)