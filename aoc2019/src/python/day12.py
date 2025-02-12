from collections import defaultdict
from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance
from itertools import count
from numpy import arctan, arctan2, pi

testInput = r"""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
input = PuzzleInput('input/day12.txt', testInput)

lines = input.getInputLines(test=False)

def part1():
    # parse to (pos, vel) tuples of (x, y, z)
    moons = [(tuple(map(lambda p: int(p[2:]), s[1:-1].split(', '))), (0, 0, 0)) for s in lines]

    for i in range(1000):
        new_moons = []
        for moon in moons:
            # calculate new velocity by adding -1, 0, or 1 to each old velocity parameter
            dv = [sum((1 if other[0][x] > moon[0][x] else -1 if other[0][x] < moon[0][x] else 0) for other in moons if other != moon) for x in range(3)]
            vel = [moon[1][p] + dv[p] for p in range(3)]

            # new position is old position + new velocity
            pos = [moon[0][p] + vel[p] for p in range(3)]

            new_moons.append((pos, vel))

        moons = new_moons

    print(moons)

    energy = sum([sum(map(abs, moon[0])) * sum(map(abs, moon[1])) for moon in moons])
    print(f'Energy: {energy}')


def part2():
    print('nyi')


runIt(part1, part2)