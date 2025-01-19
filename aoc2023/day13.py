from aoc_utils import PuzzleInput, runIt
import math
import re
import itertools

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
input = PuzzleInput('input-day13.txt', testInput)

lines = input.getInputLines(test=False)

def parsePatterns():
    patterns = []
    pattern = []
    for line in lines:
        if len(line.strip()) == 0:
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)
    return patterns

def findHorizontalReflection(p) -> int:
    # look for reflection across a horizontal line
    for i in range(len(p) - 1):
        if p[i] == p[i+1]:
            # see if the reflection extends in both directions
            above = i-1
            below = i+2
            found = True
            while above >= 0 and below < len(p):
                if (p[above] != p[below]):
                    found = False
                    break
                above -= 1
                below += 1
            if found:
                return i + 1
    return -1

def findVerticalReflection(p) -> int:
    # look for reflection across a vertical line
    for i in range(len(p[0]) - 1):
        col1 = [line[i] for line in p]
        col2 = [line[i+1] for line in p]
        
        if col1 == col2:
            # see if the reflection extends in both directions
            left = i-1
            right = i+2
            found = True
            while left >= 0 and right < len(p[0]):
                col1 = [line[left] for line in p]
                col2 = [line[right] for line in p]
                if (col1 != col2):
                    found = False
                    break
                left -= 1
                right += 1
            if found:
                return i + 1
                break
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

    # print('\n'.join(patterns[0]))
    # print('Smudged:\n')
    # for s in smudged(patterns[0]):
    #     print('\n'.join(s))
    #     print('\n')

    for p in patterns:
        origHoriz = findHorizontalReflection(p)
        origVert = findVerticalReflection(p)
        for s in smudged(p):
            h = findHorizontalReflection(s)
            if h != -1 and h != origHoriz:
                # print(f'Found horizontal line {h} in smudged\n{'\n'.join(s)}\nfrom\n{'\n'.join(p)}\n')
                horizontalCount += h
                break
            else:
                v = findVerticalReflection(s)
                if v != -1 and v != origVert:
                    # print(f'Found vertical line {h} in smudged\n{s}\nfrom\n{p}\n')
                    verticalCount += v
                    break

    total = verticalCount + (100 * horizontalCount)
    # 22297 too low
    print(f'Total {total} : {verticalCount} vertical lines, {horizontalCount} horizontal lines')

runIt(part1, part2)