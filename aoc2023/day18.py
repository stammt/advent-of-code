import aoc_utils
import math
import re
import itertools
import sys

from aoc_utils import Direction

testInput = r"""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
input = aoc_utils.PuzzleInput('input-day18.txt', testInput)

lines = input.getInputLines(test=False)

def shouldIgnoreHorizontalLine(hLine, vLine1, vLine2):
    hStart = hLine[0]
    hEnd = hLine[1]

    vLine1Start = vLine1[0] if vLine1[0] == hStart else vLine1[1]
    vLine1End = vLine1[1] if vLine1[0] == hStart else vLine1[0]
    vLine1GoesUp = vLine1End[1] < vLine1Start[1]

    vLine2Start = vLine2[0] if vLine2[0] == hEnd else vLine2[1]
    vLine2End = vLine2[1] if vLine2[0] == hEnd else vLine2[0]
    vLine2GoesUp = vLine2End[1] < vLine2Start[1]

    return vLine1GoesUp == vLine2GoesUp

# Parse the hex "color" into a pair of direction and number of steps
def directionFromHex(color):
        # trim parens and leading # from color
        color = color[2:-1]
        steps = int(color[:5], 16)
        dirInt = int(color[-1])
        dir = None
        match dirInt:
            case 0:
                dir = 'R'
            case 1:
                dir = 'D'
            case 2:
                dir = 'L'
            case 3:
                dir = 'U'
        return dir, steps

# Smarter implementation - just track the lines, then iterate through the
# rows and use each intersection to decide where the boundary of the lagoon is.
# Once we have a line with some "lagoon", jump ahead to the next horizontal
# boundary and mulitply by the number of lines in that jump since they will
# all have the same count (bounded by vertical lines).
def part2(lines):
    pos = (0, 0)
    verticalLines = set()
    horizontalLines = set()
    for line in lines:
        dir, count, color = line.split()
        dir, count = directionFromHex(color)
        print(f'Executing {dir} {count}')

        if dir == 'U' or dir == 'D':
            y = pos[1] + int(count) if dir == 'D' else pos[1] - int(count)
            pos2 = (pos[0], y)
            line = (pos, pos2) if dir == 'D' else (pos2, pos)
            verticalLines.add(line)
            pos = pos2
        else:
            x = pos[0] + int(count) if dir == 'R' else pos[0] - int(count)
            pos2 = (x, pos[1])
            line = (pos, pos2) if dir == 'R' else (pos2, pos)
            horizontalLines.add(line)
            pos = pos2

    

    # adjust the coordinates so they are all above 0,0
    allPoints = set()
    for line in horizontalLines:
        allPoints.add(line[0])
        allPoints.add(line[1])
    for line in verticalLines:
        allPoints.add(line[0])
        allPoints.add(line[1])
    minX = min(map(lambda x: x[0], allPoints))
    minY = min(map(lambda x: x[1], allPoints))
    adjX = abs(min(minX, 0))
    adjY = abs(min(minY, 0))

    maxX = max(map(lambda x: x[0], allPoints)) + adjX + 1
    maxY = max(map(lambda x: x[1], allPoints)) + adjY + 1

    adjustedVerticalLines = list(map(lambda l: ((l[0][0] + adjX, l[0][1] + adjY), (l[1][0] + adjX, l[1][1] + adjY)), verticalLines))
    adjustedHorizontalLines = list(map(lambda l: ((l[0][0] + adjX, l[0][1] + adjY), (l[1][0] + adjX, l[1][1] + adjY)), horizontalLines))

    print(f'adj horizontal: {adjustedHorizontalLines}')
    print(f'adj vertical: {adjustedVerticalLines}')

    print(f'maxX: {maxX}, maxY: {maxY}')
    # for y in range(maxY):
    #     line = []
    #     for x in range(maxX):
    #         if (x, y) in adjustedDigs:
    #             line.append('#')
    #         else:
    #             line.append('.')
    #     print(''.join(line))

    # Count the number of nodes in the edges
    edgeCount = 0
    for edge in adjustedHorizontalLines:
        edgeCount += (edge[1][0] - edge[0][0])
    for edge in adjustedVerticalLines:
        edgeCount += (edge[1][1] - edge[0][1])

    lagoonCount = 0
    # for y in range(maxY):
    y = 0
    while y < maxY:
        # horizontal lines on this line
        hLinesIntersecting = list(filter(lambda l: l[0][1] == y, adjustedHorizontalLines))
        # vertical lines that cross this line
        vLinesIntersecting = list(filter(lambda l: l[0][1] <= y and l[1][1] >= y, adjustedVerticalLines))

        # print(f'\nLines intersecting row {y}: horiz: {len(hLinesIntersecting)} vert: {len(vLinesIntersecting)}')

        # sort lines based on x value        
        hLinesIntersecting = sorted(hLinesIntersecting, key=lambda l: l[0][0])
        vLinesIntersecting = sorted(vLinesIntersecting, key=lambda l: l[0][0])
        # print(f'horiz: {hLinesIntersecting}')
        # print(f'vert: {vLinesIntersecting}')

        inLagoon = False

        x = 0
        lineLagoonCount = 0
        hasHorizIntersect = False
        while (len(hLinesIntersecting) != 0 or len(vLinesIntersecting) != 0) and x < maxX:
            # print(f'x = {x}')
            # if (len(hLinesIntersecting) > 0):
            #     print(f'First x on hLinesIntersecting: {hLinesIntersecting[0][0][0]}')
            # if (len(vLinesIntersecting) > 0):
            #     print(f'First x on vLinesIntersecting: {vLinesIntersecting[0][0][0]}')
            if len(hLinesIntersecting) > 0 and hLinesIntersecting[0][0][0] == x:
                hasHorizIntersect = True
                hLine = hLinesIntersecting[0]
                del hLinesIntersecting[0]

                # look for vertical lines at the ends, should be one on each end
                vLine1 = vLinesIntersecting[0]
                del vLinesIntersecting[0]
                vLine2 = vLinesIntersecting[0]
                del vLinesIntersecting[0]

                if (vLine1[0][0] != x):
                    print(f'The first vline did not match')
                    return
                if (vLine2[0][0] != hLine[1][0]):
                    print(f'The second vline did not match')
                    return
                
                # if both vertical lines go up or both go down, ignore this as an edge
                # print(f'Checking vertical lines {vLine1} and {vLine2}')
                ignore = shouldIgnoreHorizontalLine(hLine, vLine1, vLine2)
                # print(f'Ignoring this line? {ignore}')
                if not ignore:
                    inLagoon = not inLagoon
                x = hLine[1][0] + 1

            elif len(vLinesIntersecting) > 0 and vLinesIntersecting[0][0][0] == x:
                # Vertical line intersecting, this is always an edge crossing
                # print(f'Crossing a vertical line at x={x}')
                del vLinesIntersecting[0]
                inLagoon = not inLagoon
                x += 1

            else:
                # Jump to the next line intersection
                nextHIntersect = hLinesIntersecting[0][0][0] if len(hLinesIntersecting) > 0 else sys.maxsize
                nextVIntersect = vLinesIntersecting[0][0][0] if len(vLinesIntersecting) > 0 else sys.maxsize
                nextX = min(min(nextHIntersect, nextVIntersect), maxX)
                if inLagoon:
                    lineLagoonCount += (nextX - x)
                x  = nextX

        print(f'{lineLagoonCount} lagoon squares on line {y}\n')
        # lagoonCount += lineLagoonCount

        # See where the next horizontal line is, jump to that and add the same
        # lagoonCount for each line in between.
        nextHorizLines = sorted(list(filter(lambda l: l[0][1] > y, adjustedHorizontalLines)), key=lambda l: l[0][1])
        if len(nextHorizLines) > 0 and not hasHorizIntersect:
            nextY = nextHorizLines[0][0][1]
            print(f'Jumping ahead to line {nextY} with {lineLagoonCount} on each line')
            lagoonCount += (lineLagoonCount * (nextY - y))
            y = nextY
        else:
            # otherwise just add this line's count and move to the next line
            lagoonCount += lineLagoonCount
            y += 1
            



    if len(hLinesIntersecting) > 0 or len(vLinesIntersecting) > 0:
        print(f'Still have intersecting lines! {hLinesIntersecting} {vLinesIntersecting}')
        return
    
    print(f'Lagoon count: {lagoonCount}, edge count: {edgeCount}, total {lagoonCount + edgeCount}')

    

# Naive implementation - put all the points in a sparse matrix and count them up
def part1(lines):
    digs = set()
    pos = (0, 0)
    # digs.add(pos)
    verticalLines = set()
    horizontalLines = set()
    for line in lines:
        dir, count, color = line.split()
        # dir, count = directionFromHex(color)
        # print(f'Executing {dir} {count}')
        dx = 0
        dy = 0
        match (dir):
            case 'U':
                dy = -1
            case 'D':
                dy = 1
            case 'R':
                dx = 1
            case 'L':
                dx = -1        
        for i in range(int(count)):
            pos = (pos[0] + dx, pos[1] + dy)
            digs.add(pos)

    # adjust the coordinates so they are all above 0,0
    minX = min(map(lambda x: x[0], digs))
    minY = min(map(lambda x: x[1], digs))
    adjX = abs(min(minX, 0))
    adjY = abs(min(minY, 0))
    adjustedDigs = set(map(lambda x: (x[0] + adjX, x[1] + adjY), digs))

    maxX = max(map(lambda x: x[0], adjustedDigs)) + 1
    maxY = max(map(lambda x: x[1], adjustedDigs)) + 1

    print(f'maxX: {maxX}, maxY: {maxY}')
    # for y in range(maxY):
    #     line = []
    #     for x in range(maxX):
    #         if (x, y) in adjustedDigs:
    #             line.append('#')
    #         else:
    #             line.append('.')
    #     print(''.join(line))

    lagoon = set()
    for y in range(maxY):
        ditchCrossings = 0
        currentEdge = []
        inDitch = False
        inLagoon = False
        dbg = (y == 4)
        for x in range(maxX):
            if (x, y) in adjustedDigs:
                inDitch = True
                currentEdge.append((x, y))
            elif inDitch == True:
                if dbg is True:
                    print(f'Checking edge {currentEdge}')
                inDitch = False
                # only count if it crosses the line, not hits the line and then comes back
                # Check that the ditch extends up from one side and down from the other.
                edgeStart = currentEdge[0]
                edgeEnd = currentEdge[-1]
                if dbg:
                    print(f'Edge start and end: {edgeStart} to {edgeEnd}')
                    print(f'start: {(edgeStart[0], edgeStart[1] - 1)} {(edgeStart[0], edgeStart[1] - 1) in adjustedDigs}')
                c1 = (edgeStart[0], edgeStart[1] + 1) in adjustedDigs and (edgeEnd[0], edgeEnd[1] - 1) in adjustedDigs
                c2 = (edgeStart[0], edgeStart[1] - 1) in adjustedDigs and (edgeEnd[0], edgeEnd[1] + 1) in adjustedDigs
                if dbg is True:
                    print(f'{c1} or {c2} : {c1 or c2}')
                if (c1 or c2):
                    ditchCrossings += 1
                currentEdge = []
            inLagoon = True if inDitch == False and ditchCrossings > 0 and ditchCrossings % 2 == 1 else False
            if inLagoon == True:
                lagoon.add((x, y))

    for y in range(maxY):
        line = []
        for x in range(maxX):
            if (x, y) in adjustedDigs or (x, y) in lagoon:
                line.append('#')
            else:
                line.append('.')
        print(''.join(line))

    sum = len(adjustedDigs) + len(lagoon)
    print(f'sum {sum} : {len(adjustedDigs)} + {len(lagoon)}')
    


part2(lines)