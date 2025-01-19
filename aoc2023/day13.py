from aoc_utils import PuzzleInput, runIt
import math
import re
from itertools import groupby

testInput = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

testInput2 = """.###.#..####..#.#
.#...#.##########
#...###..##..#.#.
#...###..##..#.#.
.#...#.##########
.###.#..####..#.#
..###...#..###..#
..###...#..####.#
.###.#..####..#.#
.#...#.##########
#...###..##..#.#."""
input = PuzzleInput('input-day13.txt', testInput)

lines = input.getInputLines(test=False)

def parsePatterns():
    return [list(p) for _,p in groupby(lines, key=lambda x: x != '') if p]

def findHorizontalReflection(p, ignore=-1) -> int:
    # look for reflection across a horizontal line
    for i in range(len(p) - 1):
        if i+1 == ignore:
            continue
        dy = min(i + 1, len(p) - i - 1)
        if all([p[above] == p[below] for (above, below) in [(i-x, i+x+1) for x in range(dy)]]):
            return i+1
            
    return -1

def findVerticalReflection(p, ignore=-1) -> int:
    def col(i, p):
        return [line[i] for line in p]

    # look for reflection across a vertical line
    for i in range(len(p[0]) - 1):
        if i+1 == ignore:
            continue

        dx = min(i + 1, len(p[0]) - i - 1)
        if all([col(east, p) == col(west, p) for (east, west) in [(i-x, i+x+1) for x in range(dx)]]):
            return i+1
    return -1

def smudged(p):
    for y in range(len(p)):
        for x in range(len(p[y])):
            pcopy = [l for l in p]
            s = p[y][x]
            pcopy[y] = pcopy[y][0:x] + ('#' if s == '.' else '.') + pcopy[y][x+1:]
            yield pcopy

def part1():
    patterns = parsePatterns()

    horizontalCount = 0
    verticalCount = 0
    for p in patterns:
        h = findHorizontalReflection(p)
        if h != -1:
            horizontalCount += h
        else:
            v = findVerticalReflection(p)
            if v != -1:
                verticalCount += v

    total = verticalCount + (100 * horizontalCount)
    print(f'Total {total} : {verticalCount} vertical lines, {horizontalCount} horizontal lines')

def part2():
    patterns = parsePatterns()

    horizontalCount = 0
    verticalCount = 0

    for p in patterns:
        origHoriz = findHorizontalReflection(p)
        origVert = findVerticalReflection(p)
        for s in smudged(p):
            h = findHorizontalReflection(s, origHoriz)
            if h != -1:
                horizontalCount += h
                break
            else:
                v = findVerticalReflection(s, origVert)
                if v != -1:
                    verticalCount += v
                    break

    total = verticalCount + (100 * horizontalCount)
    print(f'Total {total} : {verticalCount} vertical lines, {horizontalCount} horizontal lines')

runIt(part1, part2)