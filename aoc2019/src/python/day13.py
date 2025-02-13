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
def read_output(output: list[int]) -> tuple[dict, int]:
    tiles = dict()
    score = -1
    i = 0
    while i < len(output):
        x = output[i]
        y = output[i+1]
        tile = output[i+2]
        if x == -1 and y == 0:
            print(f'score in tiles {tile}')
            score = tile
        else:
            tiles[(x, y)] = tile
        i += 3
    # print(f'Output: {output}')
    # print(f'Tiles: {tiles}')
    return (tiles, score)

def find_tiles(t, tiles):
    return [p for p in tiles.keys() if tiles[p] == t]

def print_tiles(tiles):
    maxx = max([p[0] for p in tiles.keys()])
    maxy = max([p[1] for p in tiles.keys()])
    for y in range(maxy + 1):
        s = ''
        for x in range(maxx + 1):
            t = tiles[(x,y)]
            if t == TILE_WALL:
                s += '#'
            elif t == TILE_BLOCK:
                s += '$'
            elif t == TILE_BALL:
                s += 'o'
            elif t == TILE_PADDLE:
                s += '_'
            else:
                s += ' '
        print(s)

def part1():
    computer = Intcode(lines[0])
    computer.run_with_input([])
    tiles, score = read_output(computer.output)
    
    blocks = len(find_tiles(TILE_BLOCK, tiles))
    print(blocks)

def part2():
    computer = Intcode(lines[0])
    computer.memory[0] = 2 # free play!
    computer.run_with_input([0])
    tiles, score = read_output(computer.output)
    print_tiles(tiles)
    
    ball = find_tiles(TILE_BALL, tiles)[0]
    old_ball = None
    paddle = find_tiles(TILE_PADDLE, tiles)[0]
    print(f'Ball: {ball}, Paddle: {paddle}')
    blocks = find_tiles(TILE_BLOCK, tiles)

    
    while len(blocks) > 0:
        move = 0
        if old_ball != None:
            move = 1 if ball[0] > old_ball[0] and paddle[0] < ball[0] else -1 if ball[0] < old_ball[0] and paddle[0] > ball[0] else 0
        # print(f'Moving {move}')
        computer.run_with_input([move])
        tiles_diff, score = read_output(computer.output)
        if computer.state == STATE_HALTED:
            print('GAME OVER MAN!')
            break

        # print(tiles_diff)
        tiles.update(tiles_diff)
        
        blocks = find_tiles(TILE_BLOCK, tiles)
        old_ball = ball
        ball = find_tiles(TILE_BALL, tiles_diff)[0]
        paddle = find_tiles(TILE_PADDLE, tiles)[0]
        # print(f'Ball: {ball}, Paddle: {paddle}, blocks: {len(blocks)}')
    

runIt(part1, part2)