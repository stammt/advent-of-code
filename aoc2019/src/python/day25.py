from collections import defaultdict
from math import ceil, floor, trunc
import os
import time
from aoc_utils import A_star, Grid, Point, PuzzleInput, get_turn, left_or_right_turn, manhattan_distance, runIt, splitInts, North, South, East, West, turn, add, cardinal_directions
from itertools import combinations, count
from intcode import STATE_HALTED, Intcode, parse_program

testInput = r""""""
input = PuzzleInput('input/day25.txt', testInput)

lines = input.getInputLines(test=False)

def all_combinations(iterable):
    items = list(iterable)
    return (
        combination
        for r in range(1, len(items) + 1)
        for combination in combinations(items, r)
    )    

def part1():
    computer = Intcode(lines[0])

    computer.run_with_input([])
    print(computer.output_as_str())

    commands = [
                # electromagnet stuck to you, can't move!
                'west',
                # 'take giant electromagnet',
                'east',

                # molten lava melts you!
                'north',
                # 'take molten lava',
                'south',

                'south',
                'take mutex',

                'south',
                'take manifold',
                'west',
                # loops, duh
                # 'take infinite loop',
                'south',
                'north',
                'west',
                'take klein bottle',
                'east',

                'east',
                'east',
                'west',
                
                'north',

                'east',
                'take mug',
                'east',
                'take polygon',
                'north',
                'take loom',

                'north',
                'take hypercube',
                'south',

                'south',
                'east',
                
                'east',
                # take escape pod to leave
                # 'take escape pod',

                # take photons, eaten by a grue!
                # 'north',
                # 'take photons',
                # 'south',

                'east',
                'take pointer',
                'south',
                'west',

                'inv']
    for c in commands:
        print(f'Command: {c}')
        computer.run_with_ascii_input([c])
        print(computer.output_as_str())

    snapshot = Intcode(computer)
    print(f'Should be at security now - taking snapshot')

    # try dropping any combination of stuff until we make it through...
    for drops in all_combinations(['mug', 'polygon', 'mutex', 'klein bottle', 'pointer', 'loom', 'manifold', 'hypercube']):
        computer = Intcode(snapshot)
        print(f'Dropping {drops}')
        for d in drops:
            computer.run_with_ascii_input([f'drop {d}'])

        computer.run_with_ascii_input(['inv'])
        print(computer.output_as_str())
        computer.run_with_ascii_input(['west'])
        s = computer.output_as_str()
        print(s)
        if s.find('Droids on this ship are lighter than') == -1 and s.find('Droids on this ship are heavier than') == -1:
            print('Got it!')
            break




def part2():
    print('no part 2')

runIt(part1, part2)