import time
import aoc_utils
import functools
import math
import re
import itertools
import sys


testInput = r"""12
14
1969
"""
input = aoc_utils.PuzzleInput('input/day01.txt', testInput)

lines = input.getInputLines(test=False)

def part1():
    result = sum(math.trunc(int(line) / 3) - 2 for line in lines)
    print(f'sum is {result}')

def fuel(mass: int) -> int:
    f = math.trunc(mass / 3) - 2
    if f <= 0:
        return 0
    return f + fuel(f)

def part2():
    result = sum(fuel(int(line)) for line in lines)
    print(f'sum is {result}')

aoc_utils.runIt(part1, part2)