from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance
from itertools import count

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

# is the candidate blocking the view from asteroid to other?
def is_blocking(candidate, asteroid, other) -> bool:
    x1, y1 = asteroid
    x2, y2 = other
    x, y = candidate

    # Check horizontal and vertical lines with no slope
    if x1 == x2:
        return x == x1 and ((y1 < y and y2 > y) or (y2 < y and y1 > y))
    
    if y1 == y2:
        return y == y1 and ((x1 < x and x2 > x) or (x2 < x and x1 > x))
    
    # Check slope intercept to see if the candidate is on the same line, then check if the candidate is
    # between them.
    # y - y1 = (y2 - y1) / (x2 - x1) * (x - x1)
    if (y - y1) == (y2 - y1) / (x2 - x1) * (x - x1):
        return ((y1 < y and y2 > y) or (y2 < y and y1 > y)) and ((x1 < x and x2 > x) or (x2 < x and x1 > x))
    return False


def part1():
    asteroids = {(x, y) for y in range(len(lines)) for x in range(len(lines[0])) if lines[y][x] == '#'}

    # for each asteroid, make a line from it to each other asteroid and see if any others are on
    # the line and "blocking" it. Track the non-blocked asteroids so we don't re-test them.
    best = (-1, -1)
    best_count = -1
    known_views = set()
    for asteroid in asteroids:
        count = 0
        for other in asteroids:
            if other == asteroid: continue

            if (asteroid, other) in known_views:
                count += 1
                continue

            # An asteroid is blocking this one if it is on the same line but closer to ours.
            blocked = False
            for candidate in asteroids:
                if candidate == other or candidate == asteroid: continue
                if is_blocking(candidate, asteroid, other):
                    blocked = True
                    break
            if not blocked:
                known_views.add((asteroid, other))
                known_views.add((other, asteroid))
                count += 1
            
        if count > best_count:
            best_count = count
            best = asteroid

    print(f'Best is {best} with a view of {best_count}')


def part2():
    print('nyi')

runIt(part1, part2)