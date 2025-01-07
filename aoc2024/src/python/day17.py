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


testInput = r"""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


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

def parse_state():
    state = {}
    state[A] = int(lines[0].split(' ')[2])
    state[B] = int(lines[1].split(' ')[2])
    state[C] = int(lines[2].split(' ')[2])
    return state

def run_program(base_state, program, subA=None) -> list[int]:
    state = dict(base_state)
    if subA != None:
        state[A] = subA
    state[OUTPUT] = []
    state[I] = 0
    while state[I] < len(program) - 1:
        iwas = state[I]
        ops[program[state[I]]](program[state[I]+1], state)
        if state[I] == iwas:
            state[I] = state[I] + 2
    return state[OUTPUT]

def part1():
    state = parse_state()
    program = splitInts(lines[4].split(' ')[1], ',')
    output = run_program(state, program)

    print(f'Output: {','.join(map(str, output))}')

# Copied from Norvig's python notebook - I was heading towards this idea but I wouldn't have come up with this
# solution on my own...
def quine(state, program) -> Set[int]:
    """Find the values of register `A` that cause the output of the run to match the program."""
    As = {0} # Set of candidate partial values for register A
    for place in reversed(range(len(program))):
        tail = list(program[place:])
        candidates = {(A1 * 8) + d for A1 in As for d in range(8)}

        As = {A1 for A1 in candidates if run_program(state, program, subA=A1) == tail}
    return As

def part2():
    state = parse_state()
    program = splitInts(lines[4].split(' ')[1], ',')
    # output = run_program(state, program, subA=0o3)
    # print(output)
    As = quine(state, program)
    print(f'Found {len(As)} candidates, min is {min(As)}')

    # sample A: 117440
    # printing A % 8 =  0,3, 5,4, 3,0
    # 0,3  A = A / 8
    # 5,4  Output A % 8
    # 3,0  Jump to 0 if A is not zero
    # 117440, 14680, 1835, 229, 28, 3, 0

    # printing B % 8, A needs to be zero at the end 2,4, 1,1, 7,5, 0,3, 4,3, 1,6, 5,5, 3,0
    # 2,4:  B = A % 8
    # 1,1:  B = B ^ 1
    # 7,5:  C = A / 2 ** B
    # 0,3:  A = A / 8
    # 4,3:  B = B ^ C
    # 1,6:  B = B ^ 6
    # 5,5:  Output B % 8
    # 3,0:  Jump to 0 or end if A is 0


runIt(part1, part2)
