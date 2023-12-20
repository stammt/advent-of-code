import aoc_utils
import math
import re
import itertools

from aoc_utils import Direction

testInput = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
input = aoc_utils.PuzzleInput('input-day16.txt', testInput)

lines = input.getInputLines(test=False)

def nextSteps(lines, step):
    tile = lines[step[1]][step[0]]
    nextStepList = []
    match tile:
        case '.':
            nextStepList = [aoc_utils.gridStep((step[0], step[1]), step[2])]
        case '/':
            nextDir = None
            match step[2]:
                case Direction.NORTH:
                    nextDir = Direction.EAST
                case Direction.EAST:
                    nextDir = Direction.NORTH
                case Direction.SOUTH:
                    nextDir = Direction.WEST
                case Direction.WEST:
                    nextDir = Direction.SOUTH
            nextStepList = [aoc_utils.gridStep((step[0], step[1]), nextDir)]
        case '\\':
            nextDir = None
            match step[2]:
                case Direction.NORTH:
                    nextDir = Direction.WEST
                case Direction.EAST:
                    nextDir = Direction.SOUTH
                case Direction.SOUTH:
                    nextDir = Direction.EAST
                case Direction.WEST:
                    nextDir = Direction.NORTH
            nextStepList = [aoc_utils.gridStep((step[0], step[1]), nextDir)]
        case '-':
            if step[2] == Direction.EAST or step[2] == Direction.WEST:
                nextStepList = [aoc_utils.gridStep((step[0], step[1]), step[2])]
            else:
                nextStepList = [aoc_utils.gridStep((step[0], step[1]), Direction.EAST), aoc_utils.gridStep((step[0], step[1]), Direction.WEST)]
        case '|':
            if step[2] == Direction.NORTH or step[2] == Direction.SOUTH:
                nextStepList = [aoc_utils.gridStep((step[0], step[1]), step[2])]
            else:
                nextStepList = [aoc_utils.gridStep((step[0], step[1]), Direction.NORTH), aoc_utils.gridStep((step[0], step[1]), Direction.SOUTH)]
        case _:
            print(f'Unknown tile {tile}')

    validNext = []
    for s in nextStepList:
        if s[0] >= 0 and s[0] < len(lines[0]) and s[1] >= 0 and s[1] < len(lines):
            validNext.append(s)
    return validNext
            
        
def part1(lines):
    q = [(0, 0, Direction.EAST)]
    energized = set()
    visited = set()
    while len(q) > 0:
        step = q[0]
        del q[0]
        if (step not in visited):
            visited.add(step)
            energized.add((step[0], step[1]))
            q = q + nextSteps(lines, step)

    print(f'{len(energized)} energized tiles') #: {energized}')
    # for y in range(len(lines)):
    #     line = ''
    #     for x in range(len(lines[0])):
    #         if (x, y) in energized:
    #             line += '#'
    #         else:
    #             line += '.'
    #     print(line)

def part2(lines):
    # Track how many tiles get energized after each step so we don't
    # have to re-trace every time -- future optimization, skipping
    # this is good enough...
    # energizedAfterStep = {}
    initialSteps = []
    for x in range(len(lines[0])):
        initialSteps.append((x, 0, Direction.SOUTH))
        initialSteps.append((x, len(lines) - 1, Direction.NORTH))
    for y in range(len(lines)):
        initialSteps.append((0, y, Direction.EAST))
        initialSteps.append((len(lines[0]) - 1, y, Direction.WEST))

    maxEnergized = 0
    for initialStep in initialSteps:
        q = [initialStep]
        energized = set()
        visited = set()
        while len(q) > 0:
            step = q[0]
            del q[0]
            if (step not in visited):
                visited.add(step)
                energized.add((step[0], step[1]))
                q = q + nextSteps(lines, step)
        maxEnergized = max(maxEnergized, len(energized))

    print(f'{maxEnergized} energized tiles')

part2(lines)