from collections import defaultdict
import sys
from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance
from itertools import count
from numpy import arctan, arctan2, pi
import math

# 01029498 after 4 phases
testInput1 = r"""12345678"""

# starts with 24176176 after 100 phases
testInput2 = r"""80871224585914546619083218645595"""
input = PuzzleInput('input/day16.txt', testInput2)

lines = input.getInputLines(test=False)
BASE_PATTERN = [0, 1, 0, -1]

def expand_pattern(d: int):
    expanded = []
    for i in BASE_PATTERN:
        for p in range(d):
            expanded.append(BASE_PATTERN[i])
    return expanded

def apply_pattern(pattern: list[int], input_digits: list[int]):
    s = 0
    p = 1
    for i in range(len(input_digits)):
        s += (input_digits[i] * pattern[p])
        p = (p + 1) % len(pattern)

    return abs(s) % 10

def solve(digits: list[int]) -> list[int]:
    t = 0
    for i in range(len(digits)):
        t += digits[i]

    updated = []
    for i in range(len(digits)):
        updated.append(t % 10)
        t -= digits[i]
    return updated


def part1():
    input_digits = list(map(int, lines[0]))
    for i in range(100):
        output_digits = []

        for d in range(len(input_digits)):
            pattern = expand_pattern(d+1)
            output_digits.append(apply_pattern(pattern, input_digits))
        input_digits = output_digits

    print(''.join(map(str, input_digits[0:8])))

def part2():
    input_digits = list(map(int, lines[0])) * 10000
    
    # trim the input to the offset
    offset = int(lines[0][:7])
    input = input_digits[offset:]
    for i in range(100):
        input = solve(input)

    print(''.join(map(str, input[0:8])))

runIt(part1, part2)