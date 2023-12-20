import aoc_utils
import math

testInput = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
input = aoc_utils.PuzzleInput('input-day10.txt', testInput)

lines = input.getInputLines(test=True)

def nextStep(lines, step):
    x = step[0]
    y = step[1]
    dir = step[2]

    tile = lines[y][x]
    nextX = -1
    nextY = -1
    nextDir = None
    match tile:
        case '|':
            nextX = x
            nextY = y - 1 if dir == 'N' else y + 1 if dir == 'S' else -1
            nextDir = 'S' if dir == 'S' else 'N' if dir == 'N' else None
        case '-':
            nextX = x - 1 if dir == 'W' else x + 1 if dir == 'E' else -1
            nextY = y
            nextDir = 'E' if dir == 'E' else 'W' if dir == 'W' else None
        case 'L':
            nextX = x if dir == 'W' else x + 1 if dir == 'S' else -1
            nextY = y - 1 if dir == 'W' else y if dir == 'S' else -1
            nextDir = 'N' if dir == 'W' else 'E' if dir == 'S' else None
        case 'J':
            nextX = x if dir == 'E' else x - 1 if dir == 'S' else -1
            nextY = y - 1 if dir == 'E' else y if dir == 'S' else -1
            nextDir = 'N' if dir == 'E' else 'W' if dir == 'S' else None
        case '7':
            nextX = x if dir == 'E' else x - 1 if dir == 'N' else -1
            nextY = y + 1 if dir == 'E' else y if dir == 'N' else -1
            nextDir = 'S' if dir == 'E' else 'W' if dir == 'N' else None
        case 'F':
            nextX = x if dir == 'W' else x + 1 if dir == 'N' else -1
            nextY = y + 1 if dir == 'W' else y if dir == 'N' else -1
            nextDir = 'S' if dir == 'W' else 'E' if dir == 'N' else None
        case '.':
            nextX = -1
            nextY = -1
            nextDir = None
        case _:
            print(f'Don''t know how to navigate {dir} from {tile} at {x}, {y}')

    # Check the bounds and return invalid if we fall off the grid
    if nextX < 0 or nextX >= len(lines[0]):
        nextX = -1
    if nextY < 0 or nextY >= len(lines):
        nextY = -1

    if nextX == -1 or nextY == -1 or nextDir == None:
        return None
    
    return (nextX, nextY, nextDir)

def move(start, dir):
    x = start[0]
    y = start[1]
    match dir:
        case 'N':
            y = y -1
        case 'S':
            y = y + 1
        case 'E':
            x = x + 1
        case 'W':
            x = x - 1
    if x < 0 or x >= len(lines[0]):
        return None
    if y < 0 or y >= len(lines):
        return None
    return (x, y)
    
def isReachable(n, pipe):
    if n in pipe:
        return False
    if n[0] < 0 or n[0] > len(lines[0]):
        return False
    if n[1] < 0 or n[1] > len(lines):
        return False
    return True

def addReachableNodes(x, y, pipe, reachable):
    # each neighbor is reachable if it is not in the pipe path,
    # and does not fall off the edge. If the neighbor is already
    # known reachable then we can stop there.
    neighbors = [
        (x-1, y-1),
        (x, y-1),
        (x+1, y-1),
        (x-1, y),
        (x+1, y),
        (x-1, y+1),
        (x, y+1),
        (x+1, y+1)
    ]
    for n in neighbors:
        if isReachable(n, pipe):
            check = n in reachable
            reachable.add(n)
            if not check:
                addReachableNodes(n[0], n[1], pipe, reachable)

class RaycastState:
    def __init__(self, edge, count, previousEdgeCount) -> None:
        self.edge = edge
        self.count = count
        self.previousEdgeCount = previousEdgeCount

    def increment(self):
        self.count = self.count + 1

# Tell if this tile can continue an edge when moving west to east
def canContinueEdge(tile, lastTile):
    if lastTile in {'-', 'F', 'L'} and tile in {'7', 'J', '-'}:
        return True
    return False
    
def startTileType(leavingDir, returningDir):
    if leavingDir == 'N':
        match returningDir:
            case 'N':
                return '|'
            case 'E':
                return 'J'
            case 'W':
                return 'L'
    if leavingDir == 'S':
        match returningDir:
            case 'S':
                return '|'
            case 'E':
                return '7'
            case 'W':
                return 'F'
    if leavingDir == 'E':
        match returningDir:
            case 'E':
                return '-'
            case 'N':
                return 'F'
            case 'S':
                return 'L'
    if leavingDir == 'W':
        match returningDir:
            case 'W':
                return '-'
            case 'N':
                return 'F'
            case 'S':
                return 'L'
            
    print(f'unknown start with leaving {leavingDir} and returning {returningDir}')

def flood(grid, pipe, start, floodedNodes):
    x = start[0]
    y = start[1]
    neighbors = [
        (x-1, y-1),
        (x, y-1),
        (x+1, y-1),
        (x-1, y),
        (x+1, y),
        (x-1, y+1),
        (x, y+1),
        (x+1, y+1)
    ]
    for n in neighbors:
        if isReachable(n, pipe):
            if (n not in floodedNodes):
                floodedNodes.add(n)
                flood(grid, pipe, n, floodedNodes)



def part1(lines):
    # Find the starting node
    start = (-1, -1)
    for y in range(len(lines)):
        x = lines[y].find('S')
        if x != -1:
            start = (x, y)
            break

    # Starting from S, traverse every possible path until we find one that
    # loops back to S from a different neighbor
    directions = ['N', 'S', 'E', 'W']
    steps = []
    for dir in directions:
        steps = []
        tile = move(start, dir)
        if (tile is None):
            continue

        step = (tile[0], tile[1], dir)

        print(f'Starting south from {start} with {step}')
        
        steps.append(step)
        while (step is not None)and (step[0] != start[0] or step[1] != start[1]):
            step = nextStep(lines, step)
            steps.append(step)

        farthest = math.floor((len(steps) + 1) / 2)
        if step is not None and (step[0] == start[0] and step[1] == start[1]):
            print(f'Found loop, starting {dir} and returning to start heading {step[2]} in {len(steps)} steps')
            print(f'Furthest is {farthest}')
            break

    # Determine the start tile type
    startTile = startTileType(dir, step[2])
    print(f'startTile {startTile}')

    pipe = set()
    for step in steps:
        pipe.add((step[0], step[1]))


    # Expand the grid to make space in the pipe that we can traverse
    expandedGrid = []
    for line in lines:
        expandedLine = []
        for i in range(len(line)):
            tile = line[i]
            expandedLine.append(tile)
            if tile == 'S':
                tile = startTile
            if tile in {'-', 'F', 'L'}:
                if i == len(line) - 1 or line[i+1] in {'7', 'J', '-'}:
                    expandedLine.append('-')
                else:
                    expandedLine.append('.')
            else:
                expandedLine.append('.')
        expandedGrid.append(''.join(expandedLine))

    fullyExpandedGrid = []
    for y in range(len(expandedGrid)):
        fullyExpandedGrid.append(expandedGrid[y])
        expandedLine = []
        for x in range(len(expandedGrid[y])):
            tileAbove = expandedGrid[y][x]
            if tileAbove == 'S':
                tileAbove = startTile
            tileBelow = None if y == len(expandedGrid) - 1 else expandedGrid[y+1][x]
            if tileBelow == 'S':
                tileBelow = startTile
            if tileAbove in {'|', 'F', '7'}:
                if tileBelow == None or tileBelow in {'|', 'J', 'L'}:
                    expandedLine.append('|')
                else:
                    expandedLine.append('.')
            else:
                expandedLine.append('.')
        fullyExpandedGrid.append(''.join(expandedLine))

    print('\n\nExpanded grid:')
    for line in fullyExpandedGrid:
        print(line)
    print('\n\n')


    # make a set of points in the expanded grid that are inside the pipe by
    # flooding the pipe starting with a point adjacent to the start node
    flood = set()

        



    # Raycasting approach: start from the edge of the graph, track if current node is
    # outside the pipe, inside the pipe, or on the edge. A node is inside the pipe if
    # there is an odd number of pipe edges after it. Collapse each line to a
    # list of (state, tileCount) and then work backwards to determine which ones
    # are "inside" the pipe: a tuple is inside if it is both before and after an odd number of
    # tile edges.
    # States True = pipe edge, False = otherwise
    # (state, tileCount, previousEdgeCount)
    # insideCount = 0
    # for y in range(len(lines)):
    #     state = None
    #     states = []
    #     previousEdgeCount = 0
    #     lastTile = ''
    #     print(f'starting line {y}')
    #     for x in range(len(lines[0])):
    #         tile = lines[y][x]
    #         if (tile == 'S'):
    #             tile = startTile
    #         if (x, y) in pipe:
    #             if state is None or state.edge == False:
    #                 print(f'starting edge at {x}')
    #                 if state is not None:
    #                     states.append(state)
    #                 state = RaycastState(True, 1, previousEdgeCount)
    #                 previousEdgeCount = previousEdgeCount + 1
    #             elif state.edge == True:
    #                 if canContinueEdge(tile, lastTile):
    #                     print(f'continuing edge at {x}')
    #                     state.increment()
    #                 else:
    #                     print(f'starting adjacent edge at {x}')
    #                     states.append(state)
    #                     state = RaycastState(True, 1, previousEdgeCount)
    #                     previousEdgeCount = previousEdgeCount + 1
    #         else:
    #             if state is None or state.edge == True:
    #                 print(f'exiting edge at {x}')
    #                 if state is not None:
    #                     states.append(state)
    #                 state = RaycastState(False, 1, previousEdgeCount)
    #             elif state.edge == False:
    #                 print(f'continuing non edge at {x}')
    #                 state.increment()
    #         lastTile = tile
            
    #     states.append(state) # get the last state
    #     # print(f'states: {states}')

    #     # go backwards through the list
    #     edgeCount = 0

    #     insideThisLine = 0
    #     for i in range(len(states) - 1, -1, -1):
    #         print(f'State {i} edge {states[i].edge} edgeCount {edgeCount} previous {states[i].previousEdgeCount}')
    #         if states[i].edge == True:
    #             edgeCount = edgeCount + 1
    #         else:
    #             # inside the pipe if we've crossed an odd number of edges and
    #             # there is an odd number of edges remaining
    #             inside = ((edgeCount % 2) == 1) and ((states[i].previousEdgeCount % 2) == 1)
    #             if inside:
    #                 insideThisLine = insideThisLine + states[i].count

    #     insideCount = insideCount + insideThisLine
    #     print(f'Found {insideThisLine} inside on line {y}\n')

    # print(f'Total inside: {insideCount}')


                



    # # Reachable nodes are outside of the pipe
    # outside = set()

    # # from the top row
    # for x in range(len(lines[0])):
    #     addReachableNodes(x, 0, pipe, outside)

    # # from the left and right edges
    # for y in range(1, len(lines) - 1):
    #     addReachableNodes(0, y, pipe, outside)
    #     addReachableNodes(len(lines[0]), y, pipe, outside)
        
    # # from the bottom row
    # for x in range(len(lines[0])):
    #     addReachableNodes(x, len(lines) - 1, pipe, outside)
    
    # # The unreachable nodes are any nodes that are not reachable and not part of the pipe itself
    # inside = set()
    # for y in range(len(lines)):
    #     for x in range(len(lines[0])):
    #         if (x, y) not in outside and (x, y) not in pipe:
    #             inside.add((x, y))
        
    # print(f'Inside count: {len(inside)}: {inside}')

part1(lines)