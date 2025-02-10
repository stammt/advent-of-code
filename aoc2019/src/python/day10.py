from collections import defaultdict
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
    # Flip the y values so they go "up" from zero
    asteroids = {(x, len(lines) - 1 - y) for y in range(len(lines)) for x in range(len(lines[0])) if lines[y][x] == '#'}

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

            # subtract the asteroid's x1,y1 to normalize to 0,0 origin for calling arctan2
            angle1 = arctan2([y2-y1], [x2-x1]) * (180 / pi)
            angles.add(angle1[0])
            
        if len(angles) > best_count:
            best_count = len(angles)
            best = (asteroid[0], len(lines) - 1 - asteroid[1])

    print(f'Best is {best} with a view of {best_count}')


def part2():
    # Flip the y values so they go "up" from zero
    asteroids = {(x, len(lines) - 1 - y) for y in range(len(lines)) for x in range(len(lines[0])) if lines[y][x] == '#'}

    # Origin is 20,18 from part 1, adjusted for the flipped view
    origin = (20, len(lines) - 1 - 18) # Test: (11, len(lines) - 1 - 13)
    
    # build a list of asteroids for each angle from the "origin"
    angles = defaultdict(list)
    x1, y1 = origin
    for other in asteroids:
        x2, y2 = other
        if other == origin: continue

        # subtract the origin's x1,y1 to normalize to 0,0 origin
        # Then add 270 so that an angle of 0 is down, which is "up" in the flipped view.
        angle1 = (arctan2([y2-y1], [x2-x1]) * (180 / pi)) + 270
        a = angle1[0]
        if a < 0:
            a = (360 + a) % 360
        angles[a % 360].append(other)

    # sort each list by distance from the origin
    for l in angles.values():
        l.sort(key = lambda x: manhattan_distance(origin, x))

    # sort the list of angles descending, since they are going counter-clockwise in the flipped world.
    angle_list = list(angles.keys())
    angle_list.sort(reverse=True)

    # Special case move angle 0 to the beginning of the list
    angle_list.remove(0)
    angle_list.insert(0, 0)

    # Loop through the angles and pop the closest asteroid from each list until we hit 200
    a = 0 # which angle
    i = 0 # how many asteroids were destroyed so far
    while True:
        l = angles[angle_list[a]]
        if len(l) > 0:
            popped = l.pop(0)
            i += 1
            if i == 200:
                adjusted = (popped[0], len(lines) - 1 - popped[1])
                print(f'200th is {adjusted} : value is {(adjusted[0] * 100) + adjusted[1]}')
                break
        a = (a + 1) % len(angle_list)


runIt(part1, part2)