import time
import aoc_utils
import functools
import math
import re
import itertools
import sys
import intcode


testInput = r"""1101,100,-1,4,0"""
input = aoc_utils.PuzzleInput('input/day05.txt', testInput)

lines = input.getInputLines(test=False)

def part1():
    ints = list(aoc_utils.splitInts(lines[0], ','))
    outputs = intcode.run_intcode(ints, [1])
    print(outputs)

def part2():
    ints = list(aoc_utils.splitInts(lines[0], ','))
    outputs = intcode.run_intcode(ints, [5])
    print(f'part2 {outputs}')

aoc_utils.runIt(part1, part2)