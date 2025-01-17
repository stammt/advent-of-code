from aoc_utils import Grid, runIt, PuzzleInput, Point, North, South, East, West, add, sub
import math

testInput = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

testInput2 = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""

testInput3 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

testInput4 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

input = PuzzleInput('input-day10.txt', testInput4)

lines = input.getInputLines(test=False)
grid = Grid(lines)
start = grid.find('S')

    
def findOutboundPipes(pos: Point, ignore: Point = (-1, -1)) -> list[Point]:
    pipes = []
    pVal = grid[pos]

    if pVal in {'S', '|', 'L', 'J'}:
        northNeighbor = add(pos, North)
        if (northNeighbor != ignore and northNeighbor in grid and grid[northNeighbor] in {'|', '7', 'F'}):
            pipes.append(northNeighbor)
    if pVal in {'S', '|', '7', 'F'}:
        southNeighbor = add(pos, South)
        if (southNeighbor != ignore and southNeighbor in grid and grid[southNeighbor] in {'|', 'L', 'J'}):
            pipes.append(southNeighbor)
    if pVal in {'S', '-', 'F', 'L'}:
        eastNeighbor = add(pos, East)
        if (eastNeighbor != ignore and eastNeighbor in grid and grid[eastNeighbor] in {'-', '7', 'J'}):
            pipes.append(eastNeighbor)
    if pVal in {'S', '-', '7', 'J'}:
        westNeighbor = add(pos, West)
        if (westNeighbor != ignore and westNeighbor in grid and grid[westNeighbor] in {'-', 'F', 'L'}):
            pipes.append(westNeighbor)
    return pipes


def part1():
    nextPipes = findOutboundPipes(start)
    print(f'Start {start}, next pipes are {nextPipes} : {grid[nextPipes[0]]} and {grid[nextPipes[1]]}')

    steps = 1
    path = [(start, start), (nextPipes[0], nextPipes[1])]
    pathOverlay = dict()
    while True:
        steps += 1
        p1 = path[1][0]
        p1Prev = path[0][0]
        p1Next = findOutboundPipes(p1, p1Prev)
        if len(p1Next) == 0:
            print(f'No next pipe from {p1}')
            break

        p2 = path[1][1]
        p2Prev = path[0][1]
        p2Next = findOutboundPipes(p2, p2Prev)
        if len(p2Next) == 0:
            print(f'No next pipe from {p1}')
            break
        
        pathOverlay[p1Next[0]] = '#' # str(steps)
        pathOverlay[p2Next[0]] = '#' #str(steps)

        if p1Next == p2Next:
            break

        path.pop(0)
        path.append((p1Next[0], p2Next[0]))

    # print(grid.to_string(pathOverlay))

    print(f'Took {steps}')

def expandFrom(p: Point, inside: set[Point], path: set[Point], grid: Grid):
    q = [p]
    while len(q) > 0:
        np = q.pop()
        if np in grid and np not in path and np not in inside:
            inside.add(np)
            for n in grid.neighbors(np, {North, South, East, West}):
                q.append(n)


def part2():
    nextPipes = findOutboundPipes(start)
    print(f'Start {start}, next pipes are {nextPipes} : {grid[nextPipes[0]]} and {grid[nextPipes[1]]}')

    path = [nextPipes[0], start, nextPipes[1]]

    # Figure out what S should be and replace it in the map
    d1 = sub(start, nextPipes[0])
    d2 = sub(start, nextPipes[1])
    dpair = {d1, d2}
    if dpair == {North, South}:
        grid[start] = '|'
    elif dpair == {East, West}:
        grid[start] = '-'
    elif dpair == {North, East}:
        grid[start] = 'L'
    elif dpair == {North, West}:
        grid[start] = 'J'
    elif dpair == {South, West}:
        grid[start] = '7'
    elif dpair == {South, East}:
        grid[start] = 'F'
    else:
        print(f'Couldnt figure out what S is {start}')

    print(f'Replaced S with {grid[start]}')
    
    # Build the path, in order
    while True:
        p1 = path[len(path)-1]
        p1Prev = path[len(path)-2]
        p1Next = findOutboundPipes(p1, p1Prev)
        if p1Next[0] == nextPipes[0]:
            break

        path.append(p1Next[0])

    # Start scanning left-to-right, top-to-bottom until we hit the path.
    # Then follow the path looking for nodes on the "other" side of the
    # pipe. For each one, flood to collect them, then continue.
    pathStart = None
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if (x,y) in path:
                pathStart = (x,y)
                break
        if pathStart != None:
            break

    if pathStart == None:
        print('never found the path!')
        return
    
    # We know the top-most left-most part of the path will be 'F', so look at the
    # next element to figure out which way we're facing, and which way is "inside".
    i = path.index(pathStart)
    facing = sub(pathStart, path[i+1])
    facingInside = South if facing == East else East

    # track path as a set for quicker lookups
    pathSet = set(path)
    inside = set()
    print(f'Starting at {pathStart} index {i} {grid[pathStart]} next is {path[i+1]} facing {facing}, inside {facingInside}')
    while True:
        i = (i+1) % len(path)
        p = path[i]
        if p == pathStart:
            break
            
        # edge case around corners, need to get "inside" with both the old facing and new facing
        if grid[p] not in {'|', '-'}:
            n = add(p, facingInside)
            expandFrom(n, inside, pathSet, grid)

            if grid[p] in {'F', 'J'}:
                if facingInside == North:
                    facingInside = West
                elif facingInside == South:
                    facingInside = East
                elif facingInside == East:
                    facingInside = South
                elif facingInside == West:
                    facingInside = North
            elif grid[p] in {'L', '7'}:
                if facingInside == North:
                    facingInside = East
                elif facingInside == South:
                    facingInside = West
                elif facingInside == East:
                    facingInside = North
                elif facingInside == West:
                    facingInside = South

        n = add(p, facingInside)
        expandFrom(n, inside, pathSet, grid)
        
    
    # 495
    print(f'Found {len(inside)}')

runIt(part1, part2)
