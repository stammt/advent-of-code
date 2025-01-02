from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  runIt, PuzzleInput, splitInts
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys


testInput = r"""125 17"""
input = PuzzleInput('input/day11.txt', testInput)
lines = input.getInputLines(test=False)

@functools.cache
def blink(stone, blinks) -> int:
    if blinks == 0:
        return 1
    
    if stone == 0:
        return blink(1, blinks - 1)
    elif len(str(stone)) %2 == 0:
        s = str(stone)
        mid = len(s) // 2
        return blink(int(s[:mid]), blinks - 1) + blink(int(s[mid:]), blinks - 1)
    else:
        return blink(2024 * stone, blinks - 1)

def part1():
    stones = splitInts(lines[0])
    c = 0
    for stone in stones:
        c += blink(stone, 25)

    print(f'total count {c}')


def part2():
    stones = splitInts(lines[0])
    c = 0
    for stone in stones:
        c += blink(stone, 75)

    print(f'total count {c}')

runIt(part1, part2)
