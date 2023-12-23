import aoc_utils
import functools
import math
import re
import itertools
import sys
from collections import Counter

testInput = r"""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
input = aoc_utils.PuzzleInput('input/input-day22.txt', testInput)

lines = input.getInputLines(test=False)

class Brick:
    def __init__(self, start, end, name):
        self.start = start
        self.end = end
        self.name = name

    def fallBy(self, dz):
        self.start[2] -= dz
        self.end[2] -= dz

    def getBottomPoints(self) -> list[(int, int)]:
        points = []
        if (self.start[0] > self.end[0]):
            print(f'x is backwards! {self}')
        if (self.start[1] > self.end[1]):
            print(f'y is backwards! {self}')
        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                points.append((x, y))
        return points
 
    def coversXY(self, x, y) -> bool:
        return (x, y) in self.getBottomPoints()
    
    def getZAtPoint(self, x, y) -> int|None:
        if not self.coversXY(x, y):
            return None
        return self.getHighestZ()
    
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
        start = aoc_utils.splitInts(start, ',')
        end = aoc_utils.splitInts(end, ',')
        bricks.append(Brick(start, end, name))
        name = chr(ord(name) + 1)
    return bricks
    
def bricksToString(bricks):
    s = []
    for b in bricks:
        s.append(str(b))
    return ''.join(s)

def howManyWouldFall(bricks, supporting):
    # Find bricks that only these bricks support
    s = set(filter(lambda x: (bricks == supporting[x]), supporting))
    fallingCount = len(s)

    # Recursively see which bricks are only supported by any combination of the ones that fell next
    if len(s) > 0:
        for l in range(len(s) + 1):
            for subset in itertools.combinations(s, l):
                fallingCount += howManyWouldFall(set(subset), supporting)
        # fallingCount += howManyWouldFall(s, supporting)

    return fallingCount

def part1(lines):
    bricks = parseBricks(lines)

    # translate the bricks down to have them fall on the ground
    fallingBricks = list(bricks)

    # bricks that have landed (on the ground or on other bricks)
    landed = []

    # map of brick -> [supporting bricks]
    supporting = {}

    # sort the falling bricks by their z index so we land the lowest
    # bricks first
    fallingBricks = sorted(fallingBricks, key=lambda b: min(b.start[2], b.end[2]))

    highestZAtPoint = {}
    highestBrickAtPoint = {}
    for brick in fallingBricks:
        # find the highest point of landed bricks for any part of
        # this brick. The bricks containing those points are supporting
        # this one when it lands.
        pointsToCheck = brick.getBottomPoints()
        highest = 0
        highestBricks = set()
        # print(f'Checking brick {b} : {pointsToCheck}')
        for p in pointsToCheck:
            pz = highestZAtPoint[p] if p in highestZAtPoint else 0
            if pz == highest:
                if pz > 0:
                    highestBricks.add(highestBrickAtPoint[p])
            elif pz > highest:
                highest = pz
                highestBricks = set()
                if pz > 0:
                    highestBricks.add(highestBrickAtPoint[p])

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
        for p in pointsToCheck:
            highestZAtPoint[p] = z
            highestBrickAtPoint[p] = brick

    ## Part 1
    # safe = 0
    # for b in landed:
    #     # Find bricks that only this brick supports
    #     s = list(filter(lambda x: (b in supporting[x] and len(supporting[x])) == 1, supporting))
    #     if len(s) == 0:
    #         safe += 1

    # print(f'Safe to disintigrate {safe} bricks')

    ## Part 2
    total = 0
    safe = 0
    for b in landed:
        sb = set()
        sb.add(b)
        fallingCount = howManyWouldFall(sb, supporting)
        print(f'{fallingCount} would fall for {b}')
        if fallingCount == 0:
            safe += 1
        else:
            total += fallingCount

    print(f'{safe} safe to remove')
    
    print(f'{total} would fall')
    #2086 too low
    #11351 too low



part1(lines)