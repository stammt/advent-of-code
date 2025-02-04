import time
from aoc_utils import Point, PuzzleInput, runIt, North, South, East, West, add, manhattan_distance
import functools
import math
import re
import itertools
import sys


testInput = r"""R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
input = PuzzleInput('input/day03.txt', testInput)

lines = input.getInputLines(test=False)

def line_points(s: str) -> tuple[set[Point], dict[Point, int]]:
    points = set()
    steps_to_point = dict()
    lastPoint = (0,0)
    stepCount = 0
    for dir in s.split(','):
        d = North if dir[0] == 'U' else South if dir[0] == 'D' else East if dir[0] == 'R' else West
        steps = int(dir[1:])
        for i in range(steps):
            lastPoint = add(lastPoint, d)
            stepCount += 1
            points.add(lastPoint)
            if lastPoint not in steps_to_point:
                steps_to_point[lastPoint] = stepCount
    return points, steps_to_point

def part1():
    line1, line1steps = line_points(lines[0])
    line2, line2steps = line_points(lines[1])
    closest = None
    closestDist = None
    for p in line1.intersection(line2):
        dist = manhattan_distance(p, (0,0))
        if closestDist == None or dist < closestDist:
            closest = p
            closestDist = dist
    print(f'Closest intersection: {closest} with distance {closestDist}')

def part2():
    line1, line1steps = line_points(lines[0])
    line2, line2steps = line_points(lines[1])
    closest = None
    closestDist = None
    for p in line1.intersection(line2):
        dist = line1steps[p] + line2steps[p]
        if closestDist == None or dist < closestDist:
            closest = p
            closestDist = dist
    print(f'Closest intersection: {closest} with step count {closestDist}')

runIt(part1, part2)