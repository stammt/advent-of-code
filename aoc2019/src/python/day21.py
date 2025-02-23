from collections import defaultdict
from math import ceil, floor, trunc
import os
import time
from aoc_utils import A_star, Grid, Point, PuzzleInput, get_turn, left_or_right_turn, manhattan_distance, runIt, splitInts, North, South, East, West, turn, add, cardinal_directions
from itertools import count
from intcode import STATE_HALTED, Intcode, parse_program

testInput = r""""""
input = PuzzleInput('input/day21.txt', testInput)

lines = input.getInputLines(test=False)

def print_grid(grid):
    os.system('clear')
    minx = min(map(lambda k: k[0], grid.keys()))
    maxx = max(map(lambda k: k[0], grid.keys()))
    miny = min(map(lambda k: k[1], grid.keys()))
    maxy = max(map(lambda k: k[1], grid.keys()))
    for y in range(miny, maxy+1):
        s = ''
        for x in range(minx, maxx+1):
            if (x, y) not in grid:
                s += ' '
            elif x == 0 and y == 0:
                s += 'S'
            else:
                s += grid[(x,y)]
        print(s)
    time.sleep(0.02)
    

def part1():
    computer = Intcode(lines[0])
    # #####.##.######## a and (not b) and d or a and b and (not c) and d
    # #####...######### (not a) and (not b) and (not c) and d OR a and (not b) and (not c) and (not d)
    # #####..########## (not a) and (not b) and c and d OR a and (not b) and (not c) and d
    # #####.########### (not a) and d OR 
    # #####.#.#########
    input = [
        'NOT A J',
        'NOT B T',
        'OR T J',
        'AND T J',
        'NOT A T',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'WALK',
        ]
    computer.run_with_ascii_input(input)
    if any([c not in range(0x110000) for c in computer.output]):
        print(computer.output)
    else:
        print(''.join((map(chr, computer.output))))

def part2():
    computer = Intcode(lines[0])
    # #####.##.######## a and (not b) and d or a and b and (not c) and d
    # #####...######### (not a) and (not b) and (not c) and d OR a and (not b) and (not c) and (not d)
    # #####..########## (not a) and (not b) and c and d OR a and (not b) and (not c) and d
    # #####.########### (not a) and d OR 
    # #####.#.#########
    # #####.#.#...#.###
    input = [
        'NOT A J',
        'NOT B T',
        'OR T J',
        'AND T J',

        'NOT A T',
        'OR T J',

        'NOT C T',
        'AND H T',
        'OR T J',

        'AND D J',

        'RUN',
        ]
    computer.run_with_ascii_input(input)
    if any([c not in range(0x110000) for c in computer.output]):
        print(computer.output)
    else:
        print(''.join((map(chr, computer.output))))

runIt(part1, part2)