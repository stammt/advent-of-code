from collections import defaultdict
import os
import time
from aoc_utils import A_star, Grid, Point, PuzzleInput, get_turn, left_or_right_turn, manhattan_distance, runIt, splitInts, North, South, East, West, turn, add, cardinal_directions
from itertools import count
from intcode import STATE_HALTED, Intcode, parse_program

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

def build_grid() -> Grid:
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
    return Grid(grid_string)
    

def part1():
    grid = build_grid()
    answer = sum([p[0] * p[1] for p in grid if is_intersection(p, grid)])
    print(f'params: {answer}')


def part2():
    grid = build_grid()
    print(grid)

    start = grid.find('^') # we know it starts facing North from part1
    facing = North

    pos = start
    steps = 0
    commands = []
    while True:
        next = add(pos, facing)
        if next in grid and grid[next] == '#':
            pos = next
            steps += 1
        else:
            if steps > 0:
                commands.append(str(steps))
                # print(commands)
                steps = 0
            next = None
            for d in left_or_right_turn(facing):
                next = add(pos, d)
                if next in grid and grid[next] == '#':
                    pos = next
                    steps += 1
                    turn_command = get_turn(facing, d)
                    commands.append(turn_command)
                    # print(commands)
                    facing = d
                    break
                else:
                    next = None

            if next == None:
                pos = None
                break
    if steps > 0:
        commands.append(str(steps))

    print(commands)

    """
    This is the output of tracing the path above:
    ['L', '10', 'R', '12', 'R', '12', 'R', '6', 'R', '10', 'L', '10', 'L', '10', 'R', '12', 'R', '12', 'R', '10', 'L', '10', 'L', '12', 'R', '6', 'R', '6', 'R', '10', 'L', '10', 'R', '10', 'L', '10', 'L', '12', 'R', '6', 'R', '6', 'R', '10', 'L', '10', 'R', '10', 'L', '10', 'L', '12', 'R', '6', 'L', '10', 'R', '12', 'R', '12', 'R', '10', 'L', '10', 'L', '12', 'R', '6']

    I just eye-balled it and came up with these three movement functions, and the routine to call them:
    [A, B, A, C, B, C, B, C, A, C]
    A = 'L', '10', 'R', '12', 'R', '12'
    B = 'R', '6', 'R', '10', 'L', '10'
    C = 'R', '10', 'L', '10', 'L', '12', 'R', '6'
    """

    modified_memory = parse_program(lines[0])
    modified_memory[0] = 2 # make it prompt for input
    routine = list(map(ord, 'A,B,A,C,B,C,B,C,A,C'))
    routine.append(10)
    fn_a = list(map(ord, 'L,10,R,12,R,12'))
    fn_a.append(10)
    fn_b = list(map(ord, 'R,6,R,10,L,10'))
    fn_b.append(10)
    fn_c = list(map(ord, 'R,10,L,10,L,12,R,6'))
    fn_c.append(10)
    video = [ord('n'), 10]
    input = [routine, fn_a, fn_b, fn_c, video]

    computer = Intcode(modified_memory)
    computer.run_with_input(routine)
    computer.run_with_input(fn_a)
    computer.run_with_input(fn_b)
    computer.run_with_input(fn_c)
    computer.run_with_input(video)

    print(computer.state)
    print(computer.output)


runIt(part1, part2)