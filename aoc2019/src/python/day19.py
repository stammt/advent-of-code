from collections import defaultdict
from math import ceil, floor, trunc
import os
import time
from aoc_utils import A_star, Grid, Point, PuzzleInput, get_turn, left_or_right_turn, manhattan_distance, runIt, splitInts, North, South, East, West, turn, add, cardinal_directions
from itertools import count
from intcode import STATE_HALTED, Intcode, parse_program

testInput = r""""""
input = PuzzleInput('input/day19.txt', testInput)

lines = input.getInputLines(test=False)

PULLED = '#'
EMPTY = '.'

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
    
def read_points(size: int):
    points = dict()
    for x in range(size):
        for y in range(size):
            computer = Intcode(lines[0])
            computer.run_with_input([x, y])
            if len(computer.output) > 0 and computer.output[0] == 1:
                points[(x, y)] = '#'
    return points

def is_in_beam(p: Point) -> bool:
    if p[0] < 0 or p[1] < 0: return False

    computer = Intcode(lines[0])
    computer.run_with_input([p[0], p[1]])
    return computer.output[0] == 1

def part1():
    points = read_points(50)
    print(len(points))

def part2():
    # We know x>100, so walk out from there, finding the top of the beam for
    # each x value. Then check if the other corner of the 100x100 box would be in the
    # beam for each point until we find one that fits. (this could be faster if done with a binary
    # search, but it's fast enough for now)
    last_x = 100
    last_top_y = 0
    while last_x < 100000:
        x = last_x + 1
        top_y = last_top_y
        while not is_in_beam((x, top_y)):
            top_y += 1

        top_left = (x-99, top_y)
        bottom_left = (x-99, top_y+99)
        if is_in_beam(bottom_left):
            print(f'Found {top_left}: {(top_left[0] * 10000) + top_left[1]}')
            break

        last_x = x
        last_top_y = top_y

    # 15231022
    print ('done')

runIt(part1, part2)