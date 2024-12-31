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
    
def get_input_section(lines:list[str], section:int) -> list[str]:
    blanks = [i for i in range(len(lines)) if len(lines[i]) == 0]
    if (section == 0):
        return lines[:blanks[0]]
    if (section == len(blanks)):
        return lines[blanks[len(blanks) - 1]+1:]
    return lines[blanks[section-1]+1 : blanks[section]]
    
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

class Grid:
    def __init__(self, lines) -> None:
        self.lines = lines
        self.max_y = len(lines)
        self.max_x = len(lines[0])

    def isInRange(self, pos) -> bool:
        return pos[1] >= 0 and pos[1] < self.max_y and pos[0] >= 0 and pos[0] < self.max_x

    
    def get(self, pos) -> Union[str, None]:
        if (not self.isInRange(pos)):
            return None
        
        return self.lines[pos[1]][pos[0]]
    
    def findAll(self, val:str) -> list[Point]:
        return [(x, y) for y in range(self.max_y) for x in range(self.max_x) if self.get((x, y)) == val ]
    
    def find(self, val:str) -> Union[Point, None]:
        all = self.findAll(val)
        if (len(all) > 0): return all[0]
        return None
    
    def neighbors(self, pos:Point, dirs) -> list[Point]:
        candidates = [add(pos, dir) for dir in dirs]
        return [c for c in candidates if self.isInRange(c)]
