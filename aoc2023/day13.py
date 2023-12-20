import aoc_utils
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
input = aoc_utils.PuzzleInput('input-day13.txt', testInput)

lines = input.getInputLines(test=False)

def part1(lines):
    patterns = []
    pattern = []
    for line in lines:
        if len(line.strip()) == 0:
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)

    print(f'Found {len(patterns)} patterns')

    horizontalCount = 0
    for p in patterns:
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
                    print(f'Found line between {i} and {i+1} in:\n{p}')
                    horizontalCount += i + 1
                    break

    verticalCount = 0
    for p in patterns:
        # look for reflection across a vertical line
        for i in range(len(p[0]) - 1):
            col1 = [line[i] for line in p]
            col2 = [line[i+1] for line in p]
            
            if col1 == col2:
                print(f'Cols {i} and {i+1} are the same {col1} -- {col2}')
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
                    print(f'-- Cols {left} and {right} are the same {col1} -- {col2}')
                    left -= 1
                    right += 1
                if found:
                    print(f'Found vertical line between {i} and {i+1} in:\n{p}')
                    verticalCount += i + 1
                    break
    total = verticalCount + (100 * horizontalCount)
    print(f'Total {total} : {verticalCount} vertical lines, {horizontalCount} horizontal lines')

part1(lines)