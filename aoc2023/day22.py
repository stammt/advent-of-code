import aoc_utils
import functools
import math
import re
import itertools
import sys

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

    def fall(self):
        self.start[2] -=1
        self.end[2] -=1

    def getBottomPoints(self) -> list[(int, int)]:
        points = []
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
    

def getHighestZAtPoint(x, y, landed) -> ((int, int), [Brick]):
    highest = 0
    highestBricks = []
    for b in landed:
        bz = b.getZAtPoint(x, y)
        if bz != None:
            if bz == highest:
                highestBricks.append(b)
            elif bz > highest:
                highest = bz
                highestBricks = [b]
    # print(f'Highest z at {x},{y} is {highest} : {bricksToString( highestBricks)}')
    return (highest, highestBricks)

def bricksToString(bricks):
    s = []
    for b in bricks:
        s.append(str(b))
    return ''.join(s)

def part1(lines):
    bricks = parseBricks(lines)

    # translate the bricks down to have them fall on the ground
    fallingBricks = list(bricks)

    # bricks that have landed (on the ground or on other bricks)
    landed = []

    # map of brick -> [supporting bricks]
    supporting = {}
    while len(fallingBricks) > 0:
        # sort the falling bricks by their z index so we land the lowest
        # bricks first
        fallingBricks = sorted(fallingBricks, key=lambda b: max(b.start[2], b.end[2]))

        # find any bricks that should stop falling - either by landing on the
        # ground (z=0) or on top of another brick that has stopped falling. 
        for b in fallingBricks:
            # find the highest point of landed bricks for any part of
            # this brick. The bricks containing those points are supporting
            # this one when it lands.
            pointsToCheck = b.getBottomPoints()
            highest = 0
            highestBricks = []
            # print(f'Checking brick {b} : {pointsToCheck}')
            for p in pointsToCheck:
                pz, hb = getHighestZAtPoint(p[0], p[1], landed)
                if pz != None:
                    if (pz == highest):
                        highestBricks += hb
                    elif pz > highest:
                        highest = pz
                        highestBricks = hb

            if b.getLowestZ() == (highest + 1):
                # the brick will land this round
                # print(f'Landed {b} supported by {bricksToString(highestBricks)}')
                landed.append(b)
                if len(highestBricks) > 0:
                    supporting[b] = highestBricks

        for b in landed:
            if b in fallingBricks:
                fallingBricks.remove(b)

        # decrement z on all of the remaining falling bricks
        print(f'Falling {len(fallingBricks)}')
        for b in fallingBricks:
            b.fall()

    safe = 0
    for b in bricks:
        # Find bricks that only this brick supports
        s = list(filter(lambda x: b in supporting[x] and len(supporting[x]) == 1, supporting))
        if len(s) == 0:
            safe += 1

    print(f'Safe to disintigrate {safe} bricks')

part1(lines)