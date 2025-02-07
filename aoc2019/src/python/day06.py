from collections import defaultdict
import time
from aoc_utils import Point, PuzzleInput, runIt, North, South, East, West, add, manhattan_distance
import functools
import math
import re
import itertools
import sys


testInput = r"""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
input = PuzzleInput('input/day06.txt', testInput)

lines = input.getInputLines(test=False)

def count_orbits(start: str, depth: int, orbits) -> int:
    return depth + sum(count_orbits(o, depth + 1, orbits) for o in orbits[start])

def find_path(start: str, path: list[str], goal: str, orbits) -> list[str]:
    if start == goal:
        return path
    
    l = orbits[start]
    for node in l:
        p = find_path(node, path + [start], goal, orbits)
        if p is not None:
            return p
        
    return None


def part1():
    orbits = defaultdict(list)
    for line in lines:
        a,b = line.split(')')
        orbits[a].append(b)

    c = count_orbits('COM', 0, orbits)
    print(c)

def part2():
    orbits = defaultdict(list)
    for line in lines:
        a,b = line.split(')')
        orbits[a].append(b)

    # find the path to YOU and SAN and strip the common prefix to find the path up the tree and then back down
    santa_path = find_path('COM', [], 'SAN', orbits)
    you_path = find_path('COM', [], 'YOU', orbits)
    while len(santa_path) > 1 and len(you_path) > 1 and santa_path[1] == you_path[1]:
        santa_path.pop(0)
        you_path.pop(0)

    # subtract 2: the first xfer is from the last node in you_path, and don't double-count the common ancestor
    c = len(santa_path) + len(you_path) - 2
    print(f'{c} transfers')

runIt(part1, part2)