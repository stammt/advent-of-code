from collections import defaultdict
import sys
from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance, cardinal_directions, add
from itertools import count
from numpy import arctan, arctan2, pi
import math

# 32768 + 2097152 = 2129920
testInput1 = r"""....#
#..#.
#..##
..#..
#...."""

input = PuzzleInput('input/day24.txt', testInput1)

lines = input.getInputLines(test=False)


def part1():
    global lines
    next_gen = lines
    seen = set()
    while True:
        seen.add(tuple(next_gen))
        gen = next_gen
        next_gen = []
        for y in range(5):
            line = []
            for x in range(5):
                neighbor_bugs = sum([1 for n in [add((x,y), d) for d in cardinal_directions] if n[0] in range(5) and n[1] in range(5) and gen[n[1]][n[0]] == '#'])
                if gen[y][x] == '#' and neighbor_bugs != 1:
                    line.append('.')
                elif gen[y][x] == '.' and neighbor_bugs in {1, 2}:
                    line.append('#')
                else:
                    line.append(gen[y][x])
            next_gen.append(tuple(line))

        if tuple(next_gen) in seen:
            print(f'Already saw this:')
            print('\n'.join(map(str, next_gen)))
            break

    i = 0
    score = 0
    for y in range(5):
        for x in range(5):
            if next_gen[y][x] == '#':
                score += (2 ** i)
            i += 1
    print(score)

def neighbors_to_check(pos: tuple[int, int, int]):
    results = []
    # add neighbors from the same level, skipping the center recursive grid at 2,2
    for d in cardinal_directions:
        n = add((pos[0], pos[1]), d)
        if n != (2, 2) and n[0] in range(5) and n[1] in range(5):
            results.append((n[0], n[1], pos[2]))

    # go to the outer grid
    if pos[0] == 0:
        results.append((1, 2, pos[2] - 1))
    elif pos[0] == 4:
        results.append((3, 2, pos[2] - 1))
    if pos[1] == 0:
        results.append((2, 1, pos[2] - 1))
    elif pos[1] == 4:
        results.append((2, 3, pos[2] - 1))
    
    # go to the inner grid
    if pos[0] == 1 and pos[1] == 2:
        for y in range(5):
            results.append((0, y, pos[2] + 1))
    elif pos[0] == 3 and pos[1] == 2:
        for y in range(5):
            results.append((4, y, pos[2] + 1))
    elif pos[0] == 2 and pos[1] == 1:
        for x in range(5):
            results.append((x, 0, pos[2] + 1))
    elif pos[0] == 2 and pos[1] == 3:
        for x in range(5):
            results.append((x, 4, pos[2] + 1))

    return results

def levels_to_check(bug_map: set):
    levels = list(map(lambda p: p[2], bug_map))
    return range(min(levels) - 1, max(levels) + 2)

def print_bugs(bug_map: set):
    levels = list(map(lambda p: p[2], bug_map))
    for z in range(min(levels), max(levels) + 1):
        print(f'Level {z}:')
        for y in range(5):
            for x in range(5):
                print('#' if (x, y, z) in bug_map else '.', end = '')
            print('')
        print('\n')

def part2():
    bug_map = set()
    # set of known bugs with coords x,y,z
    for y in range(5):
        for x in range(5):
            if lines[y][x] == '#':
                bug_map.add((x, y, 0))
    
    for minutes in range(200):
        bug_levels = levels_to_check(bug_map)
        next_gen = set()
        next_gen.update(bug_map)
        for z in bug_levels:
            for x in range(5):
                for y in range(5):
                    if (x, y) != (2, 2):
                        neighbors = neighbors_to_check((x, y, z))
                        adjacent_bug_count = sum([1 for n in neighbors if n in bug_map])
                        if (x, y, z) in bug_map and adjacent_bug_count != 1:
                            next_gen.remove((x, y, z))
                        elif (x, y, z) not in bug_map and adjacent_bug_count in {1, 2}:
                            next_gen.add((x, y, z))
        bug_map = next_gen

    print(len(bug_map))

runIt(part1, part2)