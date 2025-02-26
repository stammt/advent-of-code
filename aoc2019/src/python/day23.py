from collections import defaultdict
from math import ceil, floor, trunc
import os
import time
from aoc_utils import A_star, Grid, Point, PuzzleInput, get_turn, left_or_right_turn, manhattan_distance, runIt, splitInts, North, South, East, West, turn, add, cardinal_directions
from itertools import count
from intcode import STATE_HALTED, Intcode, parse_program

testInput = r""""""
input = PuzzleInput('input/day23.txt', testInput)

lines = input.getInputLines(test=False)
    

def part1():
    computers = [Intcode(lines[0]) for i in range(50)]
    inputs = defaultdict(list)

    # boot them up and assign addresses
    for i in range(50):
        computers[i].run_with_input([i])
        j = 0
        while j < len(computers[i].output):
            inputs[computers[i].output[j]].append((computers[i].output[j+1], computers[i].output[j+2]))
            j += 3

    while True:
        for i in range(50):
            computer = computers[i]
            input = inputs[i]
            inputs[i] = []
            if len(input) == 0:
                computer.run_with_input([-1])
            else:
                input_array = []
                for x,y in input:
                    input_array.append(x)
                    input_array.append(y)
                print(f'Computer {i} receiving input {input_array}')
                computer.run_with_input(input_array)
            j = 0
            while j < len(computer.output):
                if computers[i].output[j] == 255:
                    print(f'Sending to 255: {(computers[i].output[j+1], computers[i].output[j+2])}')
                    return
                inputs[computers[i].output[j]].append((computers[i].output[j+1], computers[i].output[j+2]))
                j += 3
            

            

def part2():
    print('nyi')

runIt(part1, part2)