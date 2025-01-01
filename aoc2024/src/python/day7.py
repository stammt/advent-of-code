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
        if (acc > value): return False
    return (acc == value)

def concat(v1:int, v2:int) -> int:
    return int(str(v1) + str(v2))

def part1():
    values = []
    for valueStr, equationStr in calibrations:
        value = int(valueStr)
        equation = splitInts(equationStr, ' ')
        slots = len(equation) - 1
        for opCombo in product([add, mul], repeat=slots):
            if checkValue(value, equation, opCombo):
                values.append(value)
                break
        
    print(f'sum {sum(values)}')

def part2():
    values = []
    for valueStr, equationStr in calibrations:
        value = int(valueStr)
        equation = splitInts(equationStr, ' ')
        slots = len(equation) - 1
        for opCombo in product([add, mul, concat], repeat=slots):
            if checkValue(value, equation, opCombo):
                values.append(value)
                break
        
    print(f'sum {sum(values)}')

runIt(part1, part2)

# my part2 takes almost 10 sec to run, see more efficient version here from norvig:
# def can_be_calibrated(equation: ints, operators=(operator.add, operator.mul)) -> bool:
#     """Can the equation be balanced using '+' and '*' operators?"""
#     target, first, *rest = equation
#     results = [first] # A list of all possible results of the partial computation
#     for y in rest:
#         results = [op(x, y) for x in results if x <= target for op in operators]
#     return target in results
