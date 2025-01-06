from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  splitInts, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys
import numpy


testInput = r"""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


input = PuzzleInput('input/day17.txt', testInput)
lines = input.getInputLines(test=False)

A = 'a'
B = 'b'
C = 'c'
OUTPUT = 'output'
I = 'i'

def op(param: int, state: dict) -> int:
    if param <= 3: return param
    elif param == 4: return state[A]
    elif param == 5: return state[B]
    elif param == 6: return state[C]
    else: return -1

def adv(param: int, state: dict) :
    state[A] = math.trunc(state[A] / (2 ** op(param, state)))

def bxl(param: int, state: dict):
    state[B] = state[B] ^ param

def bst(param: int, state: dict):
    state[B] = op(param, state) % 8

def jnz(param: int, state: dict):
    if state[A] != 0:
        state[I] = param

def bxc(param: int, state: dict):
    state[B] = state[B] ^ state[C]

def out(param: int, state: dict):
    state[OUTPUT].append(op(param, state) % 8)

def bdv(param: int, state: dict) :
    state[B] = math.trunc(state[A] / (2 ** op(param, state)))

def cdv(param: int, state: dict) :
    state[C] = math.trunc(state[A] / (2 ** op(param, state)))

ops = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}

def part1():
    state = {}
    state[A] = int(lines[0].split(' ')[2])
    state[B] = int(lines[1].split(' ')[2])
    state[C] = int(lines[2].split(' ')[2])
    state[OUTPUT] = []
    state[I] = 0

    program = splitInts(lines[4].split(' ')[1], ',')

    while state[I] < len(program) - 1:
        iwas = state[I]
        ops[program[state[I]]](program[state[I]+1], state)
        if state[I] == iwas:
            state[I] = state[I] + 2

    print(f'Output: {','.join(map(str, state[OUTPUT]))}')


def part2():
    print(f'nyi')

runIt(part1, part2)
