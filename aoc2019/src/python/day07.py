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
            output, state, pos = intcode.run_intcode(list(ints), [i, input])
            input = output[0]
            best = max(input, best)
    print(best)

def part2():
    ints = list(aoc_utils.splitInts(lines[0], ','))
    # ints = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    phase_values = [5, 6, 7, 8, 9]
    best = 0
    
    for phases in itertools.permutations(phase_values):
        amps = [intcode.Intcode(list(ints)),
                intcode.Intcode(list(ints)),
                intcode.Intcode(list(ints)),
                intcode.Intcode(list(ints)),
                intcode.Intcode(list(ints))]
        initial_run = True
        i = 0
        while True:
            amp = amps[i]
            if amp.state == intcode.STATE_HALTED:
                break
            feedback = 0 if len(amps[i-1].output) == 0 else amps[i-1].output[0]
            input = [phases[i], feedback] if initial_run else [feedback]
            amp.run_with_input(input)
            i = (i + 1) % len(phases)
            if i == 0:
                initial_run = False
        best = max(best, amps[-1].output[0])

    print(best)

aoc_utils.runIt(part1, part2)