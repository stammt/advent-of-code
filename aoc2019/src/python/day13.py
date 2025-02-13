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

# Returns (tiles, score)
def read_output(output: list[int]) -> tuple[dict[int], int]:
    tiles = defaultdict(int)
    score = 0
    i = 0
    while i < len(output):
        x = output[i]
        y = output[i+1]
        tile = output[i+2]
        if x == -1 and y == 0:
            print(f'score {tile}')
            score = tile
        elif tile != 0:
            tiles[(x, y)] = tile
        i += 3
    return (tiles, score)

def part1():
    computer = Intcode(lines[0])
    computer.run_with_input([])
    tiles, score = read_output(computer.output)
    
    blocks = len(list(filter(lambda t: t == TILE_BLOCK, tiles.values())))
    print(blocks)

def part2():
    computer = Intcode(lines[0])
    computer.memory[0] = 2 # free play!
    computer.run_with_input([0])
    tiles, score = read_output(computer.output)
    
    print(score)
    

runIt(part1, part2)