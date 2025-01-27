from collections import namedtuple
from itertools import combinations, count
import operator

import numpy
from aoc_utils import runIt, split_ints, PuzzleInput

from math import ceil, floor

testInput = r"""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
testInput2 = r"""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2"""
testInputReal = r"""328390183181243, 361677503224065, 266007888635046 @ -31, -141, 35
289605297584183, 215606437887927, 390190548172323 @ 30, 61, -138"""
input = PuzzleInput('input-day24.txt', testInput)

checkMin = 200000000000000 #7
checkMax = 400000000000000 #27

lines = input.getInputLines(test=False)

Point3 = namedtuple('Point3', 'x y z')
Point2 = namedtuple('Point2', 'x y')

class Hailstone:
    def __init__(self, line):
        point, trajectory = line.split('@')
        self.x, self.y, self.z = split_ints(point, ', ')
        self.dx, self.dy, self.dz = split_ints(trajectory, ', ')

    # Create a line segment from the current point to the edge of the
    # test area based on the trajectory.
    def createTestSegment(self, testMin, testMax):
        start = Point3(self.x, self.y, self.z)      
        stepsX = abs((testMax - self.x if self.dx > 0 else self.x - testMin) // self.dx)
        stepsY = abs((testMax - self.y if self.dy > 0 else self.y - testMin) // self.dy)
        # stepsZ = abs((testMax - self.z if self.dz > 0 else self.z - testMin) / self.dz)

        steps = min(stepsX, stepsY)
        end = Point3(self.x + (steps * self.dx), self.y + (steps * self.dy), self.z + (steps * self.dz))
        return (start, end)
    
    def pointIsInThePast(self, p: Point2):
        return (self.x < p.x and self.dx < 0) or (self.x > p.x and self.dx > 0) or (self.y < p.y and self.dy < 0) or (self.y > p.y and self.dy > 0)

    def __str__(self):
        return f'{(self.x, self.y, self.z)} - {(self.dx, self.dy, self.dz)}'


def intersect_point(stones):
    stone1, stone2 = stones

    # Figure out slope based on points in the same "order" for each line,
    # take the lowest to highest x value.
    # y = mx + b -> b = y - mx
    p1_1 = Point2(stone1.x, stone1.y)
    p1_2 = Point2(stone1.x + stone1.dx, stone1.y + stone1.dy)
    if p1_1.x > p1_2.x:
        p1_1, p1_2 = p1_2, p1_1
    m1 = (p1_2.y - p1_1.y) / (p1_2.x - p1_1.x)
    b1 = stone1.y - (m1 * stone1.x)

    p2_1 = Point2(stone2.x, stone2.y)
    p2_2 = Point2(stone2.x + stone2.dx, stone2.y + stone2.dy)
    if p2_1.x > p2_2.x:
        p2_1, p2_2 = p2_2, p2_1
    m2 = (p2_2.y - p2_1.y) / (p2_2.x - p2_1.x) 
    b2 = stone2.y - (m2 * stone2.x)

    if m1 == m2:
        return None
    
    # for the intersection set mx+b = mx+b for each line and solve for x, then y:
    # m1 * x + b1 = m2 * x + b2
    # m1 * x - m2 * x = b2 - b1
    # (m1 - m2) * x = b2 - b1
    # x = (b2 - b1) / (m1 - m2)
    x = (b2 - b1) / (m1 - m2)
    y = (m1 * x) + b1
    return Point2(x,y)

def is_valid_intersection(p: Point2, stones) -> bool:
    stone1, stone2 = stones
    if p is None: return False
    if stone1.pointIsInThePast(p) or stone2.pointIsInThePast(p): return False
    return p.x >= checkMin and p.x <= checkMax and p.y >= checkMin and p.y <= checkMax

def part1():
    hailstones = [Hailstone(line) for line in lines]

    c = sum(is_valid_intersection(intersect_point(pair), pair) for pair in combinations(hailstones, 2))

    # 16812
    print(f'{c} intersections')
    
def part2():
    hailstones = [Hailstone(line) for line in lines]

    """
    Each hailstone line is x+t*dx, y+t*dy, z+t*dz
    for the rock X+ t*DX, etc
    intersection x + t*dx = X + t*DX

    Note - re-deriving this using https://github.com/jmd-dk/advent-of-code/blob/main/2023/solution/24/solve.py
    
    use h0 as "origin", our rock hits at t=1
    P + t*V = p + t*v
    P[0] + t*V[0] = p[0] + t*v[0]
    P[1] + t*V[1] = p[1] + t*v[1]
    P[2] + t*v[2] = p[2] + t*v[2] <-- ignore for now

    Solve for t:
    t*V[0] - t*v[0] = p[0] - P[0]
    t * (V[0] - v[0]) = p[0] - P[0]
    t = (p[0] - P[0]) / (V[0] - v[0])

    Same for y, then make equal (because t=t) gives
    t = (p[1] - P[1]) / (V[1] - v[1])

    (p[0] - P[0]) / (V[0] - v[0]) = (p[1] - P[1]) / (V[1] - v[1])
    p[0] - P[0] = ((p[1] - P[1]) / (V[1] - v[1])) *  (V[0] - v[0])
    (p[0] - P[0]) * (V[1] - v[1]) = (p[1] - P[1]) * (V[0] - v[0])    
    ((V[0] - v[0]) * p[1]) - ((V[0] - v[0]) * P[1]) = ((V[1] - v[1]) * p[0]) - ((V[1] - v[1]) * P[0])
    V[0]p[1] - v[0]p[1] - V[0]P[1] + v[0]P[1] = V[1]p[0] - v[1]p[0] - V[1]P[0] + v[1]P[0]
    -V[0]P[1] + V[1]P[0] = V[1]p[0] - v[1]p[0] + v[1]P[0] - V[0]p[1] + v[0]p[1] - v[0]P[1]
    V[0]P[1] - V[1]P[0] = -V[1]p[0] + v[1]p[0] - v[1]P[0] + V[0]p[1] - v[0]p[1] + v[0]P[1]

    Finally, gives an equation independent of the chosen hailstone:
    V[0]P[1] - V[1]P[0] = p[0] * (v[1] - V[1]) + p[1] * (V[0] - v[0])  - P[0]v[1] + P[1]v[0]

    Now make equal for two hailstones i,j:
    p_i[0] * (v_i[1] - V[1]) + p_i[1] * (V[0] - v_i[0]) - P[0]v_i[1] + P[1]v_i[0] = 
    p_j[0] * (v_j[1] - V[1]) + p_j[1] * (V[0] - v_j[0]) - P[0]v_j[1] + P[1]v_j[0]

    p_i[0] * v_i[1] - p_i[0] * V[1] + p_i[1] * V[0] - p_i[1] * v_i[0] - P[0]v_i[1] + P[1]v_i[0] =
    p_j[0] * v_j[1] - p_j[0] * V[1] + p_j[1] * V[0] - p_j[1] * v_j[0] - P[0]v_j[1] + P[1]v_j[0]
    
    Move all knowns to the rhs:
    -p_i[0] * V[1] + p_i[1] * V[0] - P[0]v_i[1] + P[1]v_i[0] + p_j[0] * V[1] - p_j[1] * V[0] + P[0]v_j[1] - P[1]v_j[0] =
    -p_i[0] * v_i[1] + p_i[1] * v_i[0] + p_j[0] * v_j[1] - p_j[1] * v_j[0]

    Simplify:
    + P[0] * (v_j[1] - v_i[1])
    - P[1] * (v_j[0] - v_i[0])
    + V[1] * (p_j[0] - p_i[0])
    - V[0] * (p_j[1] - p_i[1])
    =
    - p_i[0] * v_i[1]
    + p_i[1] * v_i[0]
    + p_j[0] * v_j[1]
    - p_j[1] * v_j[0]

    Then repeat with two other hailstones to get 0,2 and 1,2 and end up with six equations for six unknowns.
    P[1] + t*V[1] = p[1] + t*v[1]
    P[2] + t*v[2] = p[2] + t*v[2]
    """
    j = 0
    rows = []
    vrows = []
    brows = []
    for i in range(2):
        j = i+ 1
        hail_i = hailstones[i] 
        hail_j = hailstones[j] 


        # P[0] P[1] P[2] V[0] V[1] V[2] 
        # Note this swaps i and j from the equations above
        rows.append([(hail_i.dy - hail_j.dy), -(hail_i.dx - hail_j.dx), 0, -(hail_i.y - hail_j.y), (hail_i.x - hail_j.x), 0])
        rows.append([-(hail_i.dz - hail_j.dz), 0, (hail_i.dx - hail_j.dx), (hail_i.z - hail_j.z), 0, -(hail_i.x - hail_j.x)])
        rows.append([0, (hail_i.dz - hail_j.dz), -(hail_i.dy - hail_j.dy), 0, -(hail_i.z - hail_j.z), (hail_i.y - hail_j.y)])

        # These are equivalent, manually derived from above or subtracting the cross-products
        vrows.append(-(hail_j.x * hail_j.dy) + (hail_j.y * hail_j.dx) + (hail_i.x * hail_i.dy) -(hail_i.y * hail_i.dx))
        vrows.append(-(hail_j.z * hail_j.dx) + (hail_j.x * hail_j.dz) + (hail_i.z * hail_i.dx) -(hail_i.x * hail_i.dz))
        vrows.append(-(hail_j.y * hail_j.dz) + (hail_j.z * hail_j.dy) + (hail_i.y * hail_i.dz) -(hail_i.z * hail_i.dy))

        brows += list(
            map(
                operator.sub,
                numpy.cross([hail_i.x, hail_i.y, hail_i.z], [hail_i.dx, hail_i.dy, hail_i.dz]),
                numpy.cross([hail_j.x, hail_j.y, hail_j.z], [hail_j.dx, hail_j.dy, hail_j.dz]),
            )
        )[::-1]

        # a2b3 - a3b2, a3b1 - a1b3, a1b2 - a2b1
        # [(hail_i.y * hail_i.dz) - (hail_i.z * hail_i.dy),
        # (hail_i.z * hail_i.dx) - (hail_i.x * hail_i.dz), 
        # (hail_i.x * hail_i.dy) - (hail_i.y * hail_i.dx)]
        # [(hail_j.y * hail_j.dz) - (hail_j.z * hail_j.dy),
        # (hail_j.z * hail_j.dx) - (hail_j.x * hail_j.dz), 
        # (hail_j.x * hail_j.dy) - (hail_j.y * hail_j.dx)]
        #
        # (hail_i.y * hail_i.dz) - (hail_i.z * hail_i.dy) - (hail_j.y * hail_j.dz) + (hail_j.z * hail_j.dy)
        # (hail_i.z * hail_i.dx) - (hail_i.x * hail_i.dz) - (hail_j.z * hail_j.dx) + (hail_j.x * hail_j.dz)
        # (hail_i.x * hail_i.dy) - (hail_i.y * hail_i.dx) - (hail_j.x * hail_j.dy) + (hail_j.y * hail_j.dx)

    print(brows)
    print(vrows)
    A = numpy.array(rows)
    P = numpy.array(vrows)
    r = numpy.linalg.solve(A, P)

    print(f'Starting {r[:3]} sum is {r[0] + r[1] + r[2]}')

runIt(part1, part2)