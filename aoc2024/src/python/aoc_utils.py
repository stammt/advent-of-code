from enum import Enum
import time
from typing import Set, Tuple, Union
from collections import defaultdict
import sys

class PuzzleInput:
    def __init__(self, fileName, testInput) -> None:
        self.fileName = fileName
        self.testInput = testInput

    # Returns a list of input lines from the test input
    def getTestInput(self) -> list[str]:
        return list(map(lambda x: x.strip(), self.testInput.splitlines()))

    # Reads the input from a file and returns a list of input lines
    def getFileInput(self) -> list[str]:
        f = open(self.fileName, 'r')
        return list(map(lambda x: x.strip(), f.readlines()))
    
    def getInputLines(self, test, mapper=None) -> list:
        lines = self.getTestInput() if test == True else self.getFileInput()
        if (mapper):
            lines = [list(map(mapper, line)) for line in lines]
        return lines

    
def get_input_section(lines:list[str], section:int) -> list[str]:
    blanks = [i for i in range(len(lines)) if len(lines[i]) == 0]
    if (section == 0):
        return lines[:blanks[0]]
    if (section == len(blanks)):
        return lines[blanks[len(blanks) - 1]+1:]
    return lines[blanks[section-1]+1 : blanks[section]]
    
def split_on_empty_lines(lines:list[str]) -> list[list[str]]:
    blanks = [i for i in range(len(lines)) if len(lines[i]) == 0]
    nextSectionStart = 0
    results = []
    for b in blanks:
        if nextSectionStart > len(lines): break
        results.append([s for s in lines[nextSectionStart:b]])
        nextSectionStart = b + 1
    if nextSectionStart <= len(lines) - 1:
        results.append([s for s in lines[nextSectionStart:]])
    return results

# Run parts 1&2 and print timing info
def runIt(part1, part2):
    p1start = time.perf_counter()
    part1()
    p1end = time.perf_counter()

    p2start = time.perf_counter()
    part2()
    p2end = time.perf_counter()

    print(f'\n---- Timing ----')
    print(f'Part 1: {((p1end - p1start)*1000):.2f}ms')
    print(f'Part 2: {((p2end - p2start)*1000):.2f}ms')

# Parse a string of space separated ints into a list of ints
def splitInts(line, separator=' ') -> Tuple[int, ...]:
    return tuple(map(int, line.strip().split(separator)))


# Point and direction helpers
Point = Tuple[int, int]

def x(pos:Point) -> int:
    return pos[0]
def y(pos:Point) -> int:
    return pos[1]

cardinal_directions = North, South, East, West = ((0, -1), (0, 1), (1, 0), (-1, 0))
cardinal_directions_moves = {'^': North, 'v': South, '>': East, '<': West}
ordinal_directions = NE, NW, SE, SW = ((1, -1), (-1, -1), (1, 1), (-1, 1))
all_directions = cardinal_directions + ordinal_directions

def add(pos:Point, dir:Point) -> Point:
    return (pos[0] + dir[0], pos[1] + dir[1])

def sub(pos:Point, dir:Point) -> Point:
    return (x(pos) - x(dir), y(pos) - y(dir))

def mul(pos:Point, k: int) -> Point:
    return (pos[0] * k, pos[1] * k)

def turn(dir:Point, turn_direction:str) -> Point:
    (x, y) = dir
    return (y, -x) if turn_direction[0] in ('L', 'l') else (-y, x)

def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Grid(dict):
    def __init__(self, lines) -> None:
        if isinstance(lines, dict):
            self.update(lines)
            maxX = max(list(map(lambda k: k[0], self.keys())))
            maxY = max(list(map(lambda k: k[1], self.keys())))
            self.size = (maxX, maxY)
        else:
            self.update({(x, y): val 
                            for y, row in enumerate(lines) 
                            for x, val in enumerate(row)})
            self.size = (max(map(len, lines)), len(lines))

    def isInRange(self, pos) -> bool:
        return pos[1] >= 0 and pos[1] < self.size[1] and pos[0] >= 0 and pos[0] < self.size[0]
    
    def findAll(self, val:str) -> list[Point]:
        return [p for p in self if self[p] == val]
    
    def find(self, val:str) -> Union[Point, None]:
        all = self.findAll(val)
        if (len(all) > 0): return all[0]
        return None
    
    def neighbors(self, pos:Point, dirs) -> list[Point]:
        candidates = [add(pos, dir) for dir in dirs]
        return [c for c in candidates if c in self]
    
    def unique_values(self, ignore={'.'}) -> Set[str]:
        return set(self.values()) - ignore
    
    def to_string(self, overlay:dict = {}) -> str:
        s = ''
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                s += overlay[(x,y)] if (x,y) in overlay else self[(x,y)]
            s += '\n'
        return s
    
    def __str__(self):
        return self.to_string()

def reconstruct_path(finish: Point, cameFrom: dict[Point, Point]) -> list[Point]:
    path = [finish]
    p = finish
    while p in cameFrom:
        p = cameFrom[p]
        path.append(p)
    path.reverse()
    return path
        
def A_star(start, goal, h, grid: Grid, wall: str = '#') -> list[Point]:
    openSet = {start} # TODO: use a priority queue or heap instead

    cameFrom: dict[Point, Point] = dict()

    # For node n, gScore[n] is the currently known cost of the cheapest path from start to n.
    gScore: dict[Point, int]  = defaultdict(lambda: sys.maxsize)
    gScore[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore: dict[Point, int] = defaultdict(lambda: sys.maxsize)
    fScore[start] = h(start)

    while len(openSet) > 0:
        current = min([n for n in openSet if n in fScore], key=lambda x: fScore[x])
        if (current == goal):
            return reconstruct_path(goal, cameFrom)
        
        openSet.remove(current)
        for n in [add(current, d) for d in cardinal_directions if add(current, d) in grid and grid[add(current, d)] != wall]:
            tentative_gScore = gScore[current] + 1 # distance is always 1 here
            if tentative_gScore < gScore[n]:
                cameFrom[n] = current
                gScore[n] = tentative_gScore
                fScore[n] = tentative_gScore + h(n)
                if n not in openSet:
                    openSet.add(n)

    return []