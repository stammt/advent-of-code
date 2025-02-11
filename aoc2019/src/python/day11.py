from collections import defaultdict
from aoc_utils import PuzzleInput, runIt, splitInts, North, South, East, West, turn, add
from itertools import count
from intcode import STATE_HALTED, Intcode

testInput = r""""""
input = PuzzleInput('input/day11.txt', testInput)

lines = input.getInputLines(test=False)

def part1():
    computer = Intcode(lines[0])
    painted = defaultdict(int)
    pos = (0,0)
    facing = North
    while computer.state != STATE_HALTED:
        computer.run_with_input([painted[pos]])
        painted[pos] = computer.output[0]
        facing = turn(facing, 'L' if computer.output[1] == 0 else 'R')
        pos = add(pos, facing)

    print(f'Painted {len(painted)}')

def part2():
    computer = Intcode(lines[0])
    painted = defaultdict(int)
    pos = (0,0)
    painted[pos] = 1
    facing = North
    while computer.state != STATE_HALTED:
        computer.run_with_input([painted[pos]])
        painted[pos] = computer.output[0]
        facing = turn(facing, 'L' if computer.output[1] == 0 else 'R')
        pos = add(pos, facing)

    minx = min(map(lambda k: k[0], painted.keys()))
    maxx = max(map(lambda k: k[0], painted.keys()))
    miny = min(map(lambda k: k[1], painted.keys()))
    maxy = max(map(lambda k: k[1], painted.keys()))
    for y in range(miny, maxy+1):
        s = ''
        for x in range(minx, maxx + 1):
            s += ('#' if painted[(x,y)] == 1 else ' ')
        print(s)


runIt(part1, part2)