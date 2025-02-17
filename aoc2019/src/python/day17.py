from collections import defaultdict
import os
import time
from aoc_utils import A_star, Grid, PuzzleInput, manhattan_distance, runIt, splitInts, North, South, East, West, turn, add, cardinal_directions
from itertools import count
from intcode import STATE_HALTED, Intcode

testInput = r""""""
input = PuzzleInput('input/day17.txt', testInput)

lines = input.getInputLines(test=False)

SCAFFOLD = '#'
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
    
def is_intersection(p, grid) -> bool:
    return grid[p] == '#' and all([add(p, d) in grid and grid[add(p, d)] == '#' for d in cardinal_directions])
    
def part1():
    computer = Intcode(lines[0])
    computer.run_with_input([])
    grid_string = []
    s = ''
    for c in computer.output:
        if c == 10:
            if len(s) > 0:
                grid_string.append(s)
            s = ''
        else:
            s += chr(c)
    if len(s) > 0:
        grid_string.append(s)
    grid = Grid(grid_string)
    print(grid)

    answer = sum([p[0] * p[1] for p in grid if is_intersection(p, grid)])
    print(f'params: {answer}')


def part2():
    computer = Intcode(lines[0])

runIt(part1, part2)