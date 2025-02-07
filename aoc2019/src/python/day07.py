import time
import aoc_utils
import functools
import math
import re
import itertools
import sys
import intcode


testInput = r"""3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"""
input = aoc_utils.PuzzleInput('input/day07.txt', testInput)

lines = input.getInputLines(test=False)

def part1():
    ints = list(aoc_utils.splitInts(lines[0], ','))
    phase_values = [0, 1, 2, 3, 4]
    best = 0
    input = 0
    for phases in itertools.permutations(phase_values):
        input = 0
        for i in phases:        
            output = intcode.run_intcode(list(ints), [i, input])
            input = output[0]
            best = max(input, best)
    print(best)

def part2():
    print('nyi')

aoc_utils.runIt(part1, part2)