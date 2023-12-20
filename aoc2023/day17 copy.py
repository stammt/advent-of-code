import aoc_utils
import math
import re
import itertools

from aoc_utils import Direction

testInput = r"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
input = aoc_utils.PuzzleInput('input-day17.txt', testInput)

lines = input.getInputLines(test=True)

oppositeDirections = {Direction.NORTH: Direction.SOUTH, Direction.SOUTH: Direction.NORTH,
                      Direction.EAST: Direction.WEST, Direction.WEST: Direction.EAST}

# Find the potential next steps given the rules:
# - can move at most three blocks in a single direction
# - cannot turn around, must go left, right, or straight
def potentialSteps(n, pathTo, lines):
    neighbors = []
    validDirs = {Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST}

    if (len(pathTo) > 1):
        validDirs.remove(oppositeDirections[pathTo[-1]])
    if len(pathTo) > 2:
        lastDir = pathTo[-1]
        if pathTo[-2] == lastDir and pathTo[-3] == lastDir:
            # print(f'Removing {lastDir} from path {pathTo}')
            validDirs.remove(lastDir)
        # else:
        #     print(f'Leaving {lastDir} in path {pathTo[:-3]}')

    print(f'\nMoving from {n} from path {pathTo} validDirs are {validDirs}')

    if (Direction.NORTH in validDirs and n[1] > 0):
        neighbors.append((n[0], n[1] - 1, Direction.NORTH))
    if (Direction.SOUTH in validDirs and n[1] < len(lines) - 1):
        neighbors.append((n[0], n[1] + 1, Direction.SOUTH))
    if (Direction.WEST in validDirs and n[0] > 0):
        neighbors.append((n[0] - 1, n[1], Direction.WEST))
    if (Direction.EAST in validDirs and n[0] < len(lines[0]) - 1):
        neighbors.append((n[0] + 1, n[1], Direction.EAST))
    print(f'Potential steps: {neighbors}')
    return neighbors


def printGridWithPath(lines, path):
    for y in range(len(lines)):
        line = []
        for x in range(len(lines[y])):
            step = list(filter(lambda node: node[0] == x and node[1] == y, path))
            if len(step) == 0:
                line += lines[y][x]
            elif x==0 and y==0:
                line += lines[y][x]
            else:
                dir = step[0][2]
                match dir:
                    case Direction.NORTH:
                        line += '^'
                    case Direction.SOUTH:
                        line += 'v'
                    case Direction.EAST:
                        line += '>'
                    case Direction.WEST:
                        line += '<'
            line += ' '
        print(''.join(line))

def shortestPathInGridQ(start, finish, lines):
    dist = {(start[0], start[1], None): 0}
    prev = {}
    q = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            q.add((x, y, Direction.NORTH))
            q.add((x, y, Direction.SOUTH))
            q.add((x, y, Direction.EAST))
            q.add((x, y, Direction.WEST))

    starting = True
    while len(q) != 0:
        # print('\n')
        u = None
        if starting == True:
            u = (start[0], start[1], None)
            starting = False
        else:
            # Get the node from q with the lowest dist value.
            qWithDist = list(filter(lambda x: x in dist, q))
            if len(qWithDist) == 0:
                break
            # print(f'qWithDist {len(qWithDist)} nodes: {qWithDist}')
            sortedQWithDist = sorted(qWithDist, key=lambda x: dist[x])
            # print(f'Nodes to process: {q}')
            print(f'SortedQ with dist: {sortedQWithDist}')
            if len(list(sortedQWithDist)) == 0:
                break
            u = sortedQWithDist[0]

            q.remove(u)
            # If this is the finish node, remove it from the q but don't
            # stop here because we need to check from other directions
            # if (u[0] == finish[0] and u[1] == finish[1]):
            #     print(f'reached finish, continuing: {u}')
            #     continue

        # debug = u[0] == 1 and u[1] == 3
        # print(f'debugging {u}')
        # Build the last 3 directions of the path to u
        p = []
        current = u
        while current != None and len(p) < 3:
            p.insert(0, current[2])
            current = prev[current] if current in prev else None


        # Find the node's n/s/e/w neighbors that are still in the q
        # p = pathTo[u] if u in pathTo else []
        neighbors = filter(lambda n: n in q, potentialSteps(u, p, lines))
        for n in neighbors:
            # the "distance" is the value of the node
            alt = dist[u] + int(lines[n[1]][n[0]])
            # print(f'checking {n} from {u} with dist {dist[u]} plus weight {alt} (vs {dist[n] if n in dist else 'none'})')

            if (n not in dist or alt < dist[n]):
                # print(f'setting {n} after {u} for weight {alt}')
                dist[n] = alt
                prev[n] = u

    # Check for paths coming into the finish from any direction
    minHeatLoss = -1
    for d in Direction:
        path = None
        n = (finish[0], finish[1], d)
        if (n not in prev):
            print(f'Couldn\'t find a path from {start} to {n}')
        else:
            print(f'Building path to finish from {d}')
            print(f'dist is {dist[n]}')
            heat = dist[n]
            path = []
            while n is not None:
                path.insert(0, n)
                n = prev[n] if n in prev else None
            # print(path)
            printGridWithPath(lines, path)
            if minHeatLoss == -1 or heat < minHeatLoss:
                minHeatLoss = heat

    print(f'minHeatLoss: {minHeatLoss}')


def shortestPathInGrid(start, finish, lines):
    dist = {(start[0], start[1], ''): 0}
    prev = {}

    # each entry in visited is (x, y, [last 3 directions to get here as a string])
    q = [(start[0], start[1], '')]
    visited = set()

    starting = True
    while len(q) != 0: 

        u = q[0]
        del q[0]
        visited.add(u)

        # If this is the finish node, remove it from the q but don't
        # stop here because we need to check from other directions
        # if (u[0] == finish[0] and u[1] == finish[1]):
        #     print(f'reached finish, continuing: {u}')
        #     continue

        # debug = u[0] == 1 and u[1] == 3
        # print(f'debugging {u}')
        # Build the last 3 directions of the path to u
        p = u[2][-3] if len(u[2]) >= 2 else []

        # Find the node's n/s/e/w neighbors that are still in the q
        # p = pathTo[u] if u in pathTo else []
        neighbors = filter(lambda n: n not in visited, potentialSteps(u, p, lines))
        for n in neighbors:
            fullPathToNList = p
            fullPathToNList.append(n[2])
            fullPathToN = ''.join(map(lambda x: str(x), fullPathToNList))
            nWithFullPath = (n[0], n[1], fullPathToN)
            if nWithFullPath in visited:
                continue

            # the "distance" is the value of the node
            alt = dist[u] + int(lines[n[1]][n[0]])
            # print(f'checking {n} from {u} with dist {dist[u]} plus weight {alt} (vs {dist[n] if n in dist else 'none'})')

            # find the previous distance for n
            replaceN = nWithFullPath not in dist or alt < dist(nWithFullPath)
            if replaceN:
                print(f'setting {n} after {u} for weight {alt}')
                prev[n] = u
                dist[nWithFullPath] = alt
                q.append(nWithFullPath)

    # Check for paths coming into the finish from any direction
    minHeatLoss = -1
    for d in Direction:
        path = None
        n = (finish[0], finish[1], d)
        if (n not in prev):
            print(f'Couldn\'t find a path from {start} to {n}')
        else:
            print(f'Building path to finish from {d}')
            print(f'dist is {dist[n]}')
            heat = dist[n]
            path = []
            while n is not None:
                path.insert(0, n)
                n = prev[n] if n in prev else None
            # print(path)
            printGridWithPath(lines, path)
            if minHeatLoss == -1 or heat < minHeatLoss:
                minHeatLoss = heat

    print(f'minHeatLoss: {minHeatLoss}')


def part1(lines):
    start = (0, 0)
    finish = (len(lines[0]) - 1, len(lines) - 1)
    # bruteForcePath(start, finish, lines)
    path = shortestPathInGrid(start, finish, lines)
    # total = 0
    # print('\nPath:')
    # for i in range(len(path)):
    #     print(f'{path[i]}')
    #     total += int(lines[path[i][0]][path[i][1]])
    # print(f'total heat loss: {total}')

    #998 too high

part1(lines)