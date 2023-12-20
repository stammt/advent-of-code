import aoc_utils
import math

testInput = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
input = aoc_utils.PuzzleInput('input-day11.txt', testInput)

lines = input.getInputLines(test=False)

def part1(lines):
    # First expand the grid by doubling all empty rows and columns
    expandedGrid = []
    # Double the empty rows
    for line in lines:
        expandedGrid.append(line)
        if '#' not in line:
            expandedGrid.append(line)

    # Double the empty columns
    # Work backwards so we don't change the indices
    for x in range(len(lines[0]) - 1, -1, -1):
        values = [line[x] for line in lines]
        if '#' not in values:
            for y in range(len(expandedGrid)):
                expandedGrid[y] = expandedGrid[y][:x] + '.' + expandedGrid[y][x:]

    print('\nOriginal grid:')
    for line in lines:
        print(line)
    print('\nExpanded grid:')
    for line in expandedGrid:
        print(line)

    # next find all the galaxies
    galaxies = []
    for y in range(len(expandedGrid)):
        for x in range(len(expandedGrid[y])):
            if expandedGrid[y][x] == '#':
                galaxies.append((x, y))

    print(f'Galaxies: {galaxies}')

    # and find all the pairs of galaxies
    galaxyPairs = set()
    for g in galaxies:
        for other in galaxies:
            # Don't add the same pair in reverse order
            if (other != g) and (other, g) not in galaxyPairs:
                galaxyPairs.add((g, other))

    print(f'Found {len(galaxyPairs)} unique pairs of galaxies')

    sum = 0
    for pair in galaxyPairs:
        # path = aoc_utils.shortestPathInGrid(pair[0], pair[1], expandedGrid)
        dist = abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
        print(f'Distance from {pair[0]} to {pair[1]} is {dist}')
        sum += dist
    print(f'sum of distances: {sum}')

def part2(lines):
    expansionFactor = 1000000

    # First find the empty rows and columns
    emptyRows = set()
    emptyCols = set()

    for y in range(len(lines)):
        if '#' not in lines[y]:
            emptyRows.add(y)

    for x in range(len(lines[0])):
        values = [line[x] for line in lines]
        if '#' not in values:
            emptyCols.add(x)

    print(f'empty rows: {emptyRows}')
    print(f'empty cols: {emptyCols}')

    # next find all the galaxies in the original grid coordinates
    galaxies = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '#':
                galaxies.append((x, y))

    print(f'Galaxies: {galaxies}')

    # and find all the pairs of galaxies
    galaxyPairs = set()
    for g in galaxies:
        for other in galaxies:
            # Don't add the same pair in reverse order
            if (other != g) and (other, g) not in galaxyPairs:
                galaxyPairs.add((g, other))

    print(f'Found {len(galaxyPairs)} unique pairs of galaxies')

    # now find the distances. For each empty row or col index that the path
    # crosses, multiply that step by the expansion factor.
    sum = 0
    for pair in galaxyPairs:
        x1, y1 = pair[0]
        x2, y2 = pair[1]
        colRange = range(min(x1, x2), max(x1, x2))
        rowRange = range(min(y1, y2), max(y1, y2))

        emptyColsInPath = [x for x in colRange if x in emptyCols]
        emptyRowsInPath = [y for y in rowRange if y in emptyRows]      

        colDist = len(colRange) + ((expansionFactor - 1) * len(emptyColsInPath))
        rowDist = len(rowRange) + ((expansionFactor - 1) * len(emptyRowsInPath))
        dist = colDist + rowDist
        sum += dist
    print(f'sum of distances: {sum}')

part2(lines)
