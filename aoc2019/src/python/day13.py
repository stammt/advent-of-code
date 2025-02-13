from collections import defaultdict
from aoc_utils import PuzzleInput, runIt, splitInts, North, South, East, West, turn, add
from itertools import count
from intcode import STATE_HALTED, Intcode

testInput = r""""""
input = PuzzleInput('input/day13.txt', testInput)

lines = input.getInputLines(test=False)

TILE_WALL = 1
TILE_BLOCK = 2
TILE_PADDLE = 3
TILE_BALL = 4

def part1():
    computer = Intcode(lines[0])
    tiles = defaultdict(int)
    computer.run_with_input([])
    i = 0
    while i < len(computer.output):
        x = computer.output[i]
        y = computer.output[i+1]
        tile = computer.output[i+2]
        if tile != 0:
            tiles[(x, y)] = tile
        i += 3
    
    blocks = len(list(filter(lambda t: t == TILE_BLOCK, tiles.values())))
    print(blocks)

def part2():
    print('nyi')

runIt(part1, part2)