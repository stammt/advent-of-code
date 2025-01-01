from operator import add, mul
import time
from typing import Set
from aoc_utils import  runIt, PuzzleInput, splitInts
import functools
import math
import re
from itertools import combinations, permutations, product
import sys


testInput = r"""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

input = PuzzleInput('input/day7.txt', testInput)

lines = input.getInputLines(test=False)
calibrations = list(map(lambda x: x.split(': '), lines))
# print(calibrations)

def checkValue(value, equation, ops) -> bool:
    acc = equation[0]
    for i, op in enumerate(ops):
        acc = op(acc, equation[i+1])
    return (acc == value)

def part1():
    values = set()
    for valueStr, equationStr in calibrations:
        value = int(valueStr)
        equation = splitInts(equationStr, ' ')
        slots = len(equation) - 1
        combos = product([add, mul], repeat=slots)
        for opCombo in combos:
            if checkValue(value, equation, opCombo):
                values.add(value)
                break
        
    print(f'sum {sum(values)}')

def part2():
    # baseVisited = findVisited()
    # c = 0
    # for p in baseVisited - {start}:
    #     if (causesLoop(p)):
    #         c+=1

    print(f'sum:')

runIt(part1, part2)