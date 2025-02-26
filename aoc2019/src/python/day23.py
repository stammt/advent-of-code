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
                computer.run_with_input(input_array)
            j = 0
            while j < len(computer.output):
                if computers[i].output[j] == 255:
                    print(f'Sending to 255: {(computers[i].output[j+1], computers[i].output[j+2])}')
                    return
                inputs[computers[i].output[j]].append((computers[i].output[j+1], computers[i].output[j+2]))
                j += 3
                        

def part2():
    computers = [Intcode(lines[0]) for i in range(50)]
    inputs = defaultdict(list)
    nat = []
    nat_sent = []

    # boot them up and assign addresses
    for i in range(50):
        computers[i].run_with_input([i])
        j = 0
        while j < len(computers[i].output):
            inputs[computers[i].output[j]].append((computers[i].output[j+1], computers[i].output[j+2]))
            j += 3

    # Track idle state, let it loop once with no inputs
    idle = False
    while True:
        if len(inputs) == 0:
            if not idle:
                idle = True
            elif len(nat) == 0:
                print('No inputs but nat is empty!')
                return
            else:
                print(f'Sending last nat packet to 0: {nat[len(nat) - 1]}')
                inputs[0].append(nat[len(nat) - 1])
                if len(nat_sent) == 2:
                    nat_sent.pop(0)
                nat_sent.append(nat[len(nat) - 1][1])
                if len(nat_sent) == 2 and nat_sent[0] == nat_sent[1]:
                    print(f'Sent value twice: {nat_sent}')
                    return
                idle = False
        else:
            print(f'Looping with {len(inputs)} inputs')
            idle = False

        for i in range(50):
            computer = computers[i]
            input = inputs[i]
            del inputs[i]
            if len(input) == 0:
                computer.run_with_input([-1])
            else:
                input_array = []
                for x,y in input:
                    input_array.append(x)
                    input_array.append(y)
                computer.run_with_input(input_array)
            j = 0
            while j < len(computer.output):
                if computers[i].output[j] == 255:
                    if len(nat) == 2:
                        nat.pop(0)
                    nat.append((computers[i].output[j+1], computers[i].output[j+2]))
                else:
                    inputs[computers[i].output[j]].append((computers[i].output[j+1], computers[i].output[j+2]))
                j += 3

runIt(part1, part2)