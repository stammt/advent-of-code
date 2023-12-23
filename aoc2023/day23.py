import aoc_utils
import functools
import math
import re
import itertools
import sys
from collections import Counter

testInput = r"""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
input = aoc_utils.PuzzleInput('input/input-day23.txt', testInput)

lines = input.getInputLines(test=False)

def getNextSteps(pos, visited, lines):
    steps = []
    if (pos[0] > 0):
        candidate = (pos[0] - 1, pos[1])
        val = lines[candidate[1]][candidate[0]]
        if candidate not in visited and (val == '.' or val == '<'):
            steps.append(candidate)
    if (pos[0] < len(lines[0]) - 1):
        candidate = (pos[0] + 1, pos[1])
        val = lines[candidate[1]][candidate[0]]
        if candidate not in visited and (val == '.' or val == '>'):
            steps.append(candidate)
    if (pos[1] > 0):
        candidate = (pos[0], pos[1] - 1)
        val = lines[candidate[1]][candidate[0]]
        if candidate not in visited and (val == '.' or val == '^'):
            steps.append(candidate)
    if (pos[1] < len(lines) - 1):
        candidate = (pos[0], pos[1] + 1)
        val = lines[candidate[1]][candidate[0]]
        if candidate not in visited and (val == '.' or val == 'v'):
            steps.append(candidate)
    return steps

class HikingPath:
    def __init__(self, start, path=[]):
        self.currentStep = start
        self.path = path

    

def allPathsDfs(start, finish, lines):
    q = [HikingPath(start, [])]

    paths = []
    while len(q) > 0:
        p = q[0]
        del q[0]

        if p.currentStep == finish:
            paths.append(p.path)
        else:
            nextSteps = getNextSteps(p.currentStep, p.path, lines)
            # Add this start node to a copy of visited, so it can be
            # visited on other traversals that may cross this one
            for step in nextSteps:
                q.append(HikingPath(step, p.path + [step]))

    return paths

def printPath(path, lines):
    for y in range(len(lines)):
        line = []
        for x in range(len(lines[0])):
            if (x, y) in path:
                line.append('O')
            else:
                line.append(lines[y][x])
        print(''.join(line))

def part1(lines):
    start = (lines[0].index('.'), 0)
    finish = (lines[len(lines) - 1].index('.'), len(lines) - 1)

    # printPath([], lines)

    allPaths = allPathsDfs(start, finish, lines)
    print(f'Found {len(allPaths)} paths')

    longestPath = []
    for p in allPaths:
        print(f'path: {len(p)}')
        if len(p) > len(longestPath):
            longestPath = p

    print(f'LongestPath: {len(longestPath)}')
    # printPath(longestPath, lines)

part1(lines)