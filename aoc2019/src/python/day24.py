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


def part2():
    print('nyi')

runIt(part1, part2)