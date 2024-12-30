import time
import aoc_utils
import functools
import math
import re
import itertools
import sys


testInput = r"""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
input = aoc_utils.PuzzleInput('input/day2.txt', testInput)

lines = input.getInputLines(test=False)

def is_safe(report:list[int]) -> bool:
    jumps = {report[i] - report[i - 1] for i in range(1, len(report))}
    return jumps.issubset({1, 2, 3}) or jumps.issubset({-1, -2, -3})

def is_safe_dampened(report:list[int]) -> bool:
    # generate all variations dropping one value
    opts = (report[:i] + report[i + 1:] for i in range(len(report)))
    return any(map(is_safe, opts))

def part1():
    reports = list(map(aoc_utils.splitInts, lines))
    c = sum(map(is_safe, reports))
    print(f'safe count {c}')

def part2():
    reports = list(map(aoc_utils.splitInts, lines))
    c = sum(map(is_safe_dampened, reports))
    print(f'dampened safe count {c}')

p1start = time.perf_counter()
part1()
p1end = time.perf_counter()

p2start = time.perf_counter()
part2()
p2end = time.perf_counter()

print(f'Part 1: {(p1end - p1start)*1000}ms')
print(f'Part 2: {(p2end - p2start)*1000}ms')