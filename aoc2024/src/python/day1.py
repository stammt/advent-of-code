import time
import aoc_utils
import functools
import math
import re
import itertools
import sys


testInput = r"""3   4
4   3
2   5
1   3
3   9
3   3
"""
input = aoc_utils.PuzzleInput('input/day1.txt', testInput)

lines = input.getInputLines(test=False)

def part1():
    pairs = list(map(lambda s: re.split('\\s+', s), lines))
    firsts = list(map(lambda p: int(p[0]), pairs))
    seconds = list(map(lambda p: int(p[1]), pairs))
    firsts.sort()
    seconds.sort()
    sum = 0
    for pair in zip(firsts, seconds):
        sum += abs(pair[0] - pair[1])
    print(f'sum is {sum}')

def part2():
    pairs = list(map(lambda s: re.split('\\s+', s), lines))
    firsts = list(map(lambda p: int(p[0]), pairs))
    seconds = list(map(lambda p: int(p[1]), pairs))
    sum = 0
    for f in firsts:
        sum += seconds.count(f) * f
    print(f'score is {sum}')

p1start = time.perf_counter()
part1()
p1end = time.perf_counter()

p2start = time.perf_counter()
part2()
p2end = time.perf_counter()

print(f'Part 1: {(p1end - p1start)*1000}ms')
print(f'Part 2: {(p2end - p2start)*1000}ms')