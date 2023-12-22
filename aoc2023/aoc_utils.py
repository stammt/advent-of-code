from enum import Enum

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
    
# Parse a string of space separated ints into a list of ints
def splitInts(line, separator=' ') -> list[int]:
    return list(map(lambda c: int(c), line.strip().split(separator)))

class Direction(Enum):
    NORTH = 1,
    SOUTH = 2,
    EAST = 3,
    WEST = 4

# Returns the next step in the given direction. Note this assumes y increases going SOUTH.
def gridStep(pos, dir):
    x = pos[0] - 1 if dir == Direction.WEST else pos[0] + 1 if dir == Direction.EAST else pos[0]
    y = pos[1] - 1 if dir == Direction.NORTH else pos[1] + 1 if dir == Direction.SOUTH else pos[1]
    return (x, y, dir)

        