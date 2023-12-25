import aoc_utils

from math import floor

testInput = r"""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
input = aoc_utils.PuzzleInput('input/input-day24.txt', testInput)

testMin = 7
testMax = 27

lines = input.getInputLines(test=True)

class Hailstone:
    def __init__(self, line):
        point, trajectory = line.split('@')
        self.x, self.y, self.z = aoc_utils.splitInts(point, ', ')
        self.dx, self.dy, self.dz = aoc_utils.splitInts(trajectory, ', ')

    # Create a line segment from the current point to the edge of the
    # test area based on the trajectory.
    def createTestSegment(self, testMin, testMax):
        start = (self.x, self.y, self.z)      
        stepsX = floor(abs((testMax - self.x if self.dx > 0 else self.x - testMin) / self.dx))
        stepsY = floor(abs((testMax - self.y if self.dy > 0 else self.y - testMin) / self.dy))
        stepsZ = floor(abs((testMax - self.z if self.dz > 0 else self.z - testMin) / self.dz))

        # For part 1 only consider x and y
        steps = min(stepsX, stepsY)
        end = (self.x + (steps * self.dx), self.y + (steps * self.dy), self.z + (steps * self.dz))
        return (start, end)

    def __str__(self):
        return f'{(self.x, self.y, self.z)} - {(self.dx, self.dy, self.dz)} - segment {self.createTestSegment(testMin, testMax)}'

def part1(lines):
    # Create line segments by extending each point to each end of the test range,
    # and then do pairwise comparisons to check for intersections.
    hailstones = []
    for line in lines:
        hailstones.append(Hailstone(line))

    for h in hailstones:
        print(str(h))
    

part1(lines)