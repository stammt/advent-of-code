from enum import Enum
import time
from typing import Tuple, Union

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
    
    def getInputLines(self, test) -> list[str]:
        return self.getTestInput() if test == True else self.getFileInput()
    
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
def splitInts(line, separator=' ') -> list[int]:
    return list(map(int, line.strip().split(separator)))


# Point and direction helpers
Point = Tuple[int, int]

def x(pos:Point) -> int:
    return pos[0]
def y(pos:Point) -> int:
    return pos[1]

cardinal_directions = North, South, East, West = ((0, -1), (0, 1), (1, 0), (-1, 0))
ordinal_directions = NE, NW, SE, SW = ((1, -1), (-1, -1), (1, 1), (-1, 1))
all_directions = cardinal_directions + ordinal_directions

def add(pos:Point, dir:Point) -> Point:
    return (x(pos) + x(dir), y(pos) + y(dir))

def sub(pos:Point, dir:Point) -> Point:
    return (x(pos) - x(dir), y(pos) - y(dir))

def mul(pos:Point, k: int) -> Point:
    return (pos[0] * k, pos[1] * k)

class Grid:
    def __init__(self, lines) -> None:
        self.lines = lines

    def isInRange(self, pos) -> bool:
        return y(pos) >= 0 and y(pos) < len(self.lines) and x(pos) >= 0 and x(pos) < len(self.lines[0])

    
    def get(self, pos) -> Union[str, None]:
        if (not self.isInRange(pos)):
            return None
        
        return self.lines[y(pos)][x(pos)]
    
    def findAll(self, val:str) -> list[Point]:
        return [(x, y) for y in range(len(self.lines)) for x in range(len(self.lines[y])) if self.get((x, y)) == val ]
    
    def neighbors(self, pos:Point, dirs) -> list[Point]:
        candidates = [add(pos, dir) for dir in dirs]
        return [c for c in candidates if self.isInRange(c)]
