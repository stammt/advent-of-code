import aoc_utils
import math
import re
import itertools
import sys

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

# entryDir: The direction we were going when we entered this segment
# travelDir: The direction we're traveling in this path segment
class PathSegment:
    def __init__(self, n, entryDir, travelDir, count):
        self.n = n
        self.entryDir = entryDir
        self.travelDir = travelDir
        self.count = count

    def getNodes(self):
        nodes = [self.n]
        if self.travelDir == Direction.NORTH or self.travelDir == Direction.SOUTH:
            dy = 1 if self.travelDir == Direction.SOUTH else -1
            for i in range(1, self.count):
                nodes.append((self.n[0], self.n[1] + (i*dy)))
        else:
            dx = 1 if self.travelDir == Direction.EAST else -1
            for i in range(1, self.count):
                nodes.append((self.n[0] + (i* dx), self.n[1]))
        return nodes
    
    def getLastNode(self):
        return self.getNodes()[-1]
    
    # gets the total heat loss for nodes in this segment
    def getHeatLoss(self, lines):
        nodes = self.getNodes()
        heatLoss = 0
        for node in nodes:
            heatLoss += int(lines[node[1]][node[0]])
        return heatLoss

    def __hash__(self):
        return hash((self.n, self.entryDir, self.travelDir, self.count))

    def __eq__(self, other):
        return self.n == other.n and self.entryDir == other.entryDir and self.travelDir == other.travelDir and self.count == other.count

    def __str__(self):
        return f'<entered {self.entryDir} traveling {self.travelDir}: {self.count} tiles starting with {self.getNodes()} ({self.getHeatLoss(lines)})>'
    
# Find the potential next path segments from entering the given
# node at the given direction. This will be 1, 2, 3 nodes in 
# orthogonal directions from the way we got to the node.
def potentialSteps(n, dir, lines):
    neighbors = []

    if dir == Direction.NORTH or dir == Direction.SOUTH:
        # all segments going east or west
        x = n[0] + 1
        path = []
        while x <= n[0] + 3 and x < len(lines[0]):
            path.append((x, n[1]))
            neighbors.append(PathSegment((n[0]+1, n[1]), dir, Direction.EAST, len(path)))
            x += 1
        x = n[0] - 1
        path = []
        while x >= n[0] - 3 and x >= 0:
            path.append((x, n[1]))
            neighbors.append(PathSegment((n[0]-1, n[1]), dir, Direction.WEST, len(path)))
            x -= 1

    if dir == Direction.EAST or dir == Direction.WEST:
        # all segments going north or south
        y = n[1] + 1
        path = []
        while y <= n[1] + 3 and y < len(lines):
            path.append((n[0], y))
            neighbors.append(PathSegment((n[0], n[1]+1), dir, Direction.SOUTH, len(path)))
            y += 1
        y = n[1] - 1
        path = []
        while y >= n[1] - 3 and y >= 0:
            path.append((n[0], y))
            neighbors.append(PathSegment((n[0], n[1]-1), dir, Direction.NORTH, len(path)))
            y -= 1

    return neighbors



def shortestPathInGrid(start, finish, lines):

    # map of path segment to previous path segment.
    prev = {}

    # path segments still to be processed - start with the start node going south and east
    q = [PathSegment(start, Direction.SOUTH, Direction.EAST, 1), PathSegment(start, Direction.EAST, Direction.SOUTH, 1)]

    # map of path segment to the total weight up until its last node
    dist = {q[0]: 0, q[1]: 0}

    # set of path segments already visited
    visited = set()

    # list of path segments that will finish the route
    finishers = []

    i = 0
    while len(q) != 0: # and i < 10:
        i+= 1 
        u = q[0]
        del q[0]
        visited.add(u)

        # if (u.n[0] > 10) or (u.n[1] > 10):
        #     print(f' at least we got to {u}')

        # print(f'\nVisited so far: {[str(item) for item in visited]}')

        # If this segment ends on the finish node, remove it from the q
        # but keep going because we need to check all paths.
        if (u.getLastNode() == finish):
            print(f'\n***Reached finish, continuing: {u}')
            finishers.append(u)
            continue

        # Find the node's n/s/e/w neighbors that are still in the q
        # p = pathTo[u] if u in pathTo else []
        neighbors = filter(lambda n: n not in visited, potentialSteps(u.getLastNode(), u.travelDir, lines))
        for n in neighbors:
            # the "distance" is the value of the node
            alt = dist[u] + n.getHeatLoss(lines)
            # print(f'checking {n} from {u} with dist {dist[u]} plus weight {alt} (vs {dist[n] if n in dist else 'none'})')

            if n not in dist or alt < dist[n]:
                # print(f'setting {n} after {u} for weight {alt}')
                prev[n] = u
                dist[n] = alt
                q.insert(0, n)

    # Check for paths coming into the finish from any direction
    minHeatLoss = sys.maxsize
    for ps in finishers:
        heatLoss = dist[ps]
        minHeatLoss = min(minHeatLoss, dist[ps])
        print(f'\n\nFound path with heat loss: {heatLoss}')
        u = ps
        while u is not None:
            print(u)
            u = prev[u] if u in prev else None

    print(f'\nminHeatLoss: {minHeatLoss}')


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