from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  A_star, manhattan_distance, splitInts, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys
import numpy


testInput = r"""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

input = PuzzleInput('input/day19.txt', testInput)
lines = input.getInputLines(test=False)

def is_possible(towel: str, patterns: list[str]) -> bool:
    for p in [p for p in patterns if towel.startswith(p)]:
        if len(towel) == len(p) or is_possible(towel[len(p):], patterns):
            return True
    return False

def count_arrangements(towel: str, patterns: list[str], counts: dict[str, int]) -> int:
    if towel in counts:
        return counts[towel]
    
    c = 0
    for p in [p for p in patterns if towel.startswith(p)]:
        if len(towel) == len(p):
            c += 1
        else:
            c += count_arrangements(towel[len(p):], patterns, counts)
    
    counts[towel] = c
    return c


def part1():
    patterns = list(lines[0].split(', '))
    patterns.sort(key=len)
    patterns.reverse()
    towels = lines[2:]

    c = sum(1 for t in towels if is_possible(t, patterns))
    print(f'Possible count {c}')


def part2():
    patterns = lines[0].split(', ')
    towels = lines[2:]

    counts = {}
    c = sum(count_arrangements(t, patterns, counts) for t in towels)
    print(f'Arrangements count {c}')
    
runIt(part1, part2)
