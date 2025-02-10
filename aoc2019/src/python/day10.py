from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance
from itertools import count
from numpy import arctan, arctan2, pi

testInput = r""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
input = PuzzleInput('input/day10.txt', testInput)

lines = input.getInputLines(test=False)


def part1():
    # Normalize the y values so they go "up" from zero
    asteroids = {(x, len(lines) - y) for y in range(len(lines)) for x in range(len(lines[0])) if lines[y][x] == '#'}

    # for each asteroid, find the angles to every other asteroid and track the unique values. (if multiple other
    # asteroids are at the same angle, we only see the closest one)
    best = (-1, -1)
    best_count = -1
    for asteroid in asteroids:
        angles = set()
        x1, y1 = asteroid
        for other in asteroids:
            x2, y2 = other
            if other == asteroid: continue

            # subtract the asteroid's x1,y1 to normalize to 0,0 origin
            angle1 = arctan2([y2-y1], [x2-x1]) * (180 / pi)
            angles.add(angle1[0])
            
        # print(f'Found {count} vs {len(angles)} angles')
        if len(angles) > best_count:
            best_count = len(angles)
            best = asteroid

    print(f'Best is {best} with a view of {best_count}')


def part2():
    print('nyi')

def angles():
    for asteroid in asteroids:
        x1, y1 = asteroid
        angles = set()
        for other in asteroids:
            if other == asteroid: continue

            x2, y2 = other

            if (x1 == x2):
                angles.add(0 if y1 < y2 else 180)
            elif (y1 == y2):
                angles.add(90 if x1 < x2 else 270)
            else:
                slope = (y2 - y1) / (x2 - x1)
                angle = round((arctan(slope) * (180 / math.pi)) + 90, 4)
                print(f'adding angle {angle} from {asteroid} to {other}')
                angles.add(angle)
            
        if len(angles) > best_count:
            best_count = len(angles)
            best = asteroid

runIt(part1, part2)