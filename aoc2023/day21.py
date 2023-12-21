import aoc_utils
import functools
import math
import re
import itertools
import sys

testInput = r"""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
input = aoc_utils.PuzzleInput('input/input-day21.txt', testInput)

lines = input.getInputLines(test=False)

def addIfPlot(pos, plots, lines):
    if pos[0] >= 0 and pos[0] < len(lines[0]) and pos[1] >= 0 and pos[1] < len(lines) and (lines[pos[1]][pos[0]] == '.' or lines[pos[1]][pos[0]] == 'S'):
        plots.append(pos)
    
def getNeighborPlots(pos, lines):
    neighbors = []
    addIfPlot((pos[0] - 1, pos[1]), neighbors, lines)
    addIfPlot((pos[0] + 1, pos[1]), neighbors, lines)
    addIfPlot((pos[0], pos[1] - 1), neighbors, lines)
    addIfPlot((pos[0], pos[1] + 1), neighbors, lines)
    return neighbors

def printMap(plots, lines):
    for y in range(len(lines)):
        line = []
        for x in range(len(lines[0])):
            if (x, y) in plots:
                line.append('O')
            else:
                line.append(lines[y][x])

        print(''.join(line))

def part1(lines):
    start = None
    for y in range(len(lines)):
        x = lines[y].find('S')
        if x != -1:
            start = (x, y)
            break

    stepGoal = 64
    plots = set()
    plots.add(start)

    for i in range(stepGoal):
        q = list(plots)
        plots = set()

        while len(q) > 0:
            step = q[0]
            del q[0]

            neighbors = getNeighborPlots(step, lines)
            for n in neighbors:
                plots.add(n)
        # print(f'\nAfter step {i}')
        # printMap(plots, lines)

    print(f'Hit {len(plots)}')


part1(lines)