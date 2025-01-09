from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  A_star, sliding_window, splitInts, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, groupby, permutations, product
import sys
import numpy


testInput = r"""1
10
100
2024"""

input = PuzzleInput('input/day22.txt', testInput)
lines = input.getInputLines(test=False)


def mix(secret: int, value: int) -> int:
    return secret ^ value

def prune(secret: int) -> int:
    return secret % 16777216

def next_secret(secret: int) -> int:
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret

def part1():
    sum = 0
    for line in lines:
        secret = int(line)
        for i in range(2000):
            secret = next_secret(secret)
        sum += secret
    print(f'sum: {sum}')

def part2():
    print('nyi')

runIt(part1, part2)
