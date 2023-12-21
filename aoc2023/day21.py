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

lines = input.getInputLines(test=True)

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

def addIfInfinitePlot(pos, plots, lines):
    x, y = mapToCentralGrid(pos, lines)

    # print(f'Mapping {pos} to {x},{y} in {len(lines)} x {len(lines[0])} grid')

    if lines[y][x] == '.' or lines[y][x] == 'S':
        plots.append(pos)

def getInfiniteNeighborPlots(pos, lines):
    neighbors = []
    addIfInfinitePlot((pos[0] - 1, pos[1]), neighbors, lines)
    addIfInfinitePlot((pos[0] + 1, pos[1]), neighbors, lines)
    addIfInfinitePlot((pos[0], pos[1] - 1), neighbors, lines)
    addIfInfinitePlot((pos[0], pos[1] + 1), neighbors, lines)
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

def mapToCentralGrid(pos, lines):
    x = pos[0]
    if x < 0:
        m = (abs(x) % len(lines[0]))
        if m == 0:
            x = 0
        else:
            x = len(lines[0]) - m
    elif x >= len(lines[0]):
        x = x % len(lines[0])

    y = pos[1]
    if y < 0:
        m = (abs(y) % len(lines))
        if m == 0:
            y = 0
        else:
            y = len(lines) - m
    elif y >= len(lines):
        y = y % len(lines)

    return (x, y)

def part2(lines):
    start = None
    for y in range(len(lines)):
        x = lines[y].find('S')
        if x != -1:
            start = (x, y)
            break

    stepGoal = 10
    plots = set()
    plots.add(start)
    plotCounts = {start: 1}

    # After each round, reduce the plots back to the central grid,
    # with a count of how many paths would have reached that point.

    for i in range(stepGoal):
        q = list(plots)
        plots = set()
        previousPlotCounts = plotCounts
        plotCounts = {}

        print(f'\nStep {i}')
        while len(q) > 0:
            step = q[0]
            del q[0]

            previousCount = previousPlotCounts[step] 
            print(f'Stepping from {step}, x {previousCount}')
            neighbors = getInfiniteNeighborPlots(step, lines)
            for n in neighbors:
                plots.add(n)
                plotCounts[n] = previousCount

        mappedPlots = set()
        mappedPlotCounts = {}
        for p in plotCounts:
            mapped = mapToCentralGrid(p, lines)
            count = plotCounts[p]

            if p != mapped:
                count += plotCounts[mapped] if mapped in plotCounts else 0
            mappedPlotCounts[mapped] = count
            mappedPlots.add(mapped)

        plots = mappedPlots
        plotCounts = mappedPlotCounts

        # print(f'\nAfter step {i}')
        # printMap(plots, lines)
    total = 0
    for plot in plots:
        total += plotCounts[plot]

    print(f'Hit {total}')

part2(lines)