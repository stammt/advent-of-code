from aoc_utils import PuzzleInput, split_ints, runIt
import functools
import math
import re
import itertools
import sys
from collections import Counter, defaultdict

testInput = r"""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
input = PuzzleInput('input-day22.txt', testInput)

lines = input.getInputLines(test=False)

class Brick:
    def __init__(self, start, end, name):
        self.start = start
        self.end = end
        self.name = name
        self.bottom_points = {(x,y) for x in range(self.start[0], self.end[0] + 1) for y in range(self.start[1], self.end[1] + 1)}

    def fallBy(self, dz):
        self.start[2] -= dz
        self.end[2] -= dz
 
    def overlapsXY(self, brick) -> bool:
        return not self.bottom_points.isdisjoint(brick.bottom_points)
    
    def coversXY(self, x, y) -> bool:
        return (x, y) in self.bottom_points
        
    def getHighestZ(self) -> int:
        return max(self.start[2], self.end[2])
    
    def getLowestZ(self) -> int:
        return min(self.start[2], self.end[2])
    
    def __str__(self):
        return '<' + self.name + ': ' + str(self.start) + ' ~ ' + str(self.end) + '>'
    
def parseBricks(lines) -> list[Brick]:
    bricks = []
    name = 'A'
    for line in lines:
        start, end = line.split('~')
        start = split_ints(start, ',')
        end = split_ints(end, ',')
        bricks.append(Brick(start, end, name))
        name = chr(ord(name) + 1)
    return bricks
    
def bricksToString(bricks):
    s = []
    for b in bricks:
        s.append(str(b))
    return ''.join(s)

def howManyWouldFall(disintegrated: set[Brick], supporting):
    # Find bricks only supported by these bricks
    s = list(filter(lambda x: x not in disintegrated and disintegrated.issuperset(supporting[x]), supporting))

    # Recursively see which bricks are only supported by any combination of the ones that have already
    # disintegrated, stopping when no more fall.
    disintegrated.update(s)
    if len(s) > 0:
        howManyWouldFall(disintegrated, supporting)

def part1():
    bricks = parseBricks(lines)

    # translate the bricks down to have them fall on the ground
    fallingBricks = list(bricks)

    # bricks that have landed (on the ground or on other bricks)
    landed = []

    # map of brick -> set[supporting bricks]
    supporting = {}

    # sort the falling bricks by their z index so we land the lowest
    # bricks first
    fallingBricks = sorted(fallingBricks, key=lambda b: min(b.start[2], b.end[2]))

    highestZAtPoint = defaultdict(int)
    for brick in fallingBricks:
        # find the highest point of landed bricks for any part of
        # this brick. The bricks containing those points are supporting
        # this one when it lands.
        highest = max(highestZAtPoint[p] for p in brick.bottom_points)

        # bricks that are at the highest z and overlap this brick's x,y will be supporting this brick
        highestBricks = set(filter(lambda b: b.getHighestZ() == highest and b.overlapsXY(brick), landed))

        # drop this brick by enough that it's lowest point will be
        # one higher than the highest point.
        dz = brick.getLowestZ() - (highest + 1)
        # print(f'falling {brick} by {dz} - checked {pointsToCheck} and got {highest}')
        brick.fallBy(dz)
        landed.append(brick)

        if len(highestBricks) > 0:
            supporting[brick] = highestBricks

        # update the highest points with this brick
        z = brick.getHighestZ()
        for p in brick.bottom_points:
            highestZAtPoint[p] = z

    # Part 1
    safe = 0
    for b in landed:
        # Find bricks that only this brick supports
        s = list(filter(lambda x: (b in supporting[x] and len(supporting[x])) == 1, supporting))
        if len(s) == 0:
            safe += 1

    print(f'Safe to disintigrate {safe} bricks')

    ## Part 2
    total = 0
    for b in landed:
        disintegrated = set()
        disintegrated.add(b)
        howManyWouldFall(disintegrated, supporting)
        fallingCount = len(disintegrated) - 1
        # print(f'{fallingCount} would fall for {b}')
        total += fallingCount
    
    #41610
    print(f'{total} would fall')

def part2():
    print('nyi')


runIt(part1, part2)
