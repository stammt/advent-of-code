from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  runIt, PuzzleInput, split_on_empty_lines, splitInts, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys
import numpy


testInput = r"""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

input = PuzzleInput('input/day13.txt', testInput)
lines = input.getInputLines(test=False)

# parse into button A, button B, prize
def parse_machine(lines:list[str]) -> tuple:
    a = tuple(map(lambda x: int(x[2:]), lines[0].split(': ')[1].split(', ')))
    b = tuple(map(lambda x: int(x[2:]), lines[1].split(': ')[1].split(', ')))
    prize = tuple(map(lambda x: int(x[2:]), lines[2].split(': ')[1].split(', ')))
    return (a, b, prize)

# I don't even...
def close_enough(a) -> bool:
    i = round(a)
    return abs(a - i) < 0.0001

def part1():
    machines = [parse_machine(s) for s in split_on_empty_lines(lines)]
    price = 0
    # print(f'found {len(machines)} machines (*4 is {len(machines) * 4})')
    for m in machines:
        # (a * m[0][0]) + (b * m[1][0]) = prize[0]
        # (a * m[0][1]) + (b * m[1][1]) = prize[1]
        A = numpy.array([[m[0][0], m[1][0]],
                         [m[0][1], m[1][1]]])
        Ai = numpy.linalg.inv(A)
        P = numpy.array([[m[2][0]], [m[2][1]]])
        r = numpy.dot(Ai, P)
        # print(r)
        if close_enough(r[0][0]) and close_enough(r[1][0]):
            price += (round(r[0][0]) * 3) + round(r[1][0])

    print(f'total price {price}')


def part2():
    machines = [parse_machine(s) for s in split_on_empty_lines(lines)]
    price = 0
    # print(f'found {len(machines)} machines (*4 is {len(machines) * 4})')
    for m in machines:
        # (a * m[0][0]) + (b * m[1][0]) = prize[0]
        # (a * m[0][1]) + (b * m[1][1]) = prize[1]
        A = numpy.array([[m[0][0], m[1][0]],
                         [m[0][1], m[1][1]]])
        P = numpy.array([[10000000000000 + m[2][0]], [10000000000000 + m[2][1]]])
        r = numpy.linalg.solve(A, P)
        # print(r)
        a = r[0][0]
        b = r[1][0]
        if close_enough(a) and close_enough(b):
            price += (round(a) * 3) + round(b)


    print(f'total price {price}')

runIt(part1, part2)
