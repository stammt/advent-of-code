from collections import defaultdict
import sys
from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance
from itertools import count
from numpy import arctan, arctan2, pi
import math

testInput1 = r"""<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
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
    # parse to (pos, vel) tuples of (x, y, z)
    moons = [(list(map(lambda p: int(p[2:]), s[1:-1].split(', '))), [0, 0, 0]) for s in lines]

    # Save the original x, y, and z positions. We're going to find when they get back to the original
    # position on each axis, with a zero velocity for that axis, then find the lcm of those step counts
    # to find when all three will be back to the original. Note the example seemed to have multiple
    # cycle lengths for some variables we we just store all of the times that they repeat until we have
    # at least one for each.
    original_pos_x = [moon[0][0] for moon in moons]
    original_pos_y = [moon[0][1] for moon in moons]
    original_pos_z = [moon[0][2] for moon in moons]
    x_period = []
    y_period = []
    z_period = []
    for i in range(1, 30000000):
        new_moons = []
        for moon in moons:
            # calculate new velocity by adding -1, 0, or 1 to each old velocity parameter
            dv = [sum((1 if other[0][x] > moon[0][x] else -1 if other[0][x] < moon[0][x] else 0) for other in moons if other != moon) for x in range(3)]
            vel = [moon[1][p] + dv[p] for p in range(3)]

            # new position is old position + new velocity
            pos = [moon[0][p] + vel[p] for p in range(3)]

            new_moons.append((pos, vel))

        moons = new_moons
        new_pos_x = [moon[0][0] for moon in moons]
        vel_x = [moon[1][0] for moon in moons]
        new_pos_y = [moon[0][1] for moon in moons]
        vel_y = [moon[1][1] for moon in moons]
        new_pos_z = [moon[0][2] for moon in moons]
        vel_z = [moon[1][2] for moon in moons]
        if new_pos_x == original_pos_x and vel_x == [0, 0, 0, 0]:
            print(f'x equals at {i}')
            x_period.append(i)
        if new_pos_y == original_pos_y and vel_y == [0, 0, 0, 0]:
            print(f'y equals at {i}')
            y_period.append(i)
        if new_pos_z == original_pos_z and vel_z == [0, 0, 0, 0]:
            print(f'z equals at {i}')
            z_period.append(i)

        if len(x_period) > 0 and len(y_period) > 0 and len(z_period) > 0:
            break

    answer = sys.maxsize
    for xp in range(len(x_period)):
        for yp in range(len(y_period)):
            for zp in range(len(z_period)):
                a = math.lcm(x_period[xp], y_period[yp], z_period[zp])
                answer = min(answer, a)
    print(f'Answer: {answer}')

runIt(part1, part2)