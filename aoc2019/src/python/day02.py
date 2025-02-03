import time
import aoc_utils
import functools
import math
import re
import itertools
import sys


testInput = r"""1,1,1,4,99,5,6,0,99"""
input = aoc_utils.PuzzleInput('input/day02.txt', testInput)

lines = input.getInputLines(test=False)

def part1():
    ints = list(aoc_utils.splitInts(lines[0], ','))
    ints[1] = 12
    ints[2] = 2
    i = 0
    while True:
        op = ints[i]
        if op == 99:
            break
        op1 = ints[ints[i+1]]
        op2 = ints[ints[i+2]]
        val = op1 + op2 if op == 1 else op1 * op2
        ints[ints[i+3]] = val
        i += 4

    print(f'After running: {ints}')

def part2():
    memory = list(aoc_utils.splitInts(lines[0], ','))
    noun = 0
    verb = 0
    target = 19690720
    for noun in range(100):
        for verb in range(100):
            ints = list(memory)
            ints[1] = noun
            ints[2] = verb
            i = 0
            while True:
                op = ints[i]
                if op == 99:
                    break
                op1 = ints[ints[i+1]]
                op2 = ints[ints[i+2]]
                val = op1 + op2 if op == 1 else op1 * op2
                ints[ints[i+3]] = val
                i += 4
            if ints[0] == target:
                print(f'Hit target with {(100*noun) + verb}')
                return

aoc_utils.runIt(part1, part2)