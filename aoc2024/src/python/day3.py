from operator import mul
import time
import aoc_utils
import functools
import math
import re
import itertools
import sys


testInput = r"""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
input = aoc_utils.PuzzleInput('input/day3.txt', testInput)

lines = input.getInputLines(test=False)
line = ''.join(lines)
p = re.compile(r'mul\((\d+),(\d+)\)')

def part1():
    c = sum(map(lambda expr: mul(*map(int, expr.group(1, 2))), p.finditer(line)))
    print(f'sum {c}')

def part2():
    enabled = True
    c = 0
    for mulMatch in p.finditer(line):
        lastDo = line[:mulMatch.span()[0]].rfind('do()')
        lastDont = line[:mulMatch.span()[0]].rfind('don\'t()')
        if (lastDont > lastDo):
            enabled = False
        else:
            enabled = True

        if enabled:
            c += mul(*map(int, mulMatch.group(1, 2)))

    print(f'sum {c}')


p1start = time.perf_counter()
part1()
p1end = time.perf_counter()

p2start = time.perf_counter()
part2()
p2end = time.perf_counter()

print(f'Part 1: {(p1end - p1start)*1000}ms')
print(f'Part 2: {(p2end - p2start)*1000}ms')