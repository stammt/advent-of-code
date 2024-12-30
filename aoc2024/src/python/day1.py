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
    pairs = list(map(lambda s: map(int, re.split('\\s+', s)), lines))
    firsts, seconds = zip(*pairs)
    total = sum(abs(a-b) for a,b in zip(sorted(firsts), sorted(seconds)))
    print(f'sum is {total}')

def part2():
    pairs = list(map(lambda s: map(int, re.split('\\s+', s)), lines))
    firsts, seconds = zip(*pairs)
    total = sum(a * seconds.count(a) for a in firsts)
    print(f'score is {total}')

p1start = time.perf_counter()
part1()
p1end = time.perf_counter()

p2start = time.perf_counter()
part2()
p2end = time.perf_counter()

print(f'-- Timing:')
print(f'Part 1: {(p1end - p1start)*1000}ms')
print(f'Part 2: {(p2end - p2start)*1000}ms')