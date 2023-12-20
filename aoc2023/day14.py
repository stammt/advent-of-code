import aoc_utils
import math
import re
import itertools

testInput = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
input = aoc_utils.PuzzleInput('input-day14.txt', testInput)

lines = input.getInputLines(test=False)

def tiltNorth(tilted):
    for x in range(len(lines[0])):
        y = len(lines) - 1
        rolling = []
        while y >= 0:
            c = tilted[y][x]
            if c == '#' or y == 0:
                # put down any rocks that are rolling
                # print('stop')
                # print(f'Putting down {len(rolling)} rocks at {y}, {x}')
                for i in range(len(rolling)):
                    tilted[rolling[i]][x] = '.'
                adj = 1 if c != '.' else 0
                for i in range(len(rolling)):
                    tilted[y+i+adj][x] = 'O'
                rolling = []
            elif c == 'O':
                # pick up another rolling rock
                # print('picked up another')
                # print(f'Picked up rock at {y}, {x}')
                rolling.append(y)

            y-=1

    return tilted

def tiltSouth(tilted):
    for x in range(len(lines[0])):
        y = 0
        rolling = []
        while y < len(lines):
            c = tilted[y][x]
            if c == '#' or y == len(lines) - 1:
                # put down any rocks that are rolling
                # print('stop')
                # print(f'Putting down {len(rolling)} rocks at {y}, {x}')
                for i in range(len(rolling)):
                    tilted[rolling[i]][x] = '.'
                adj = 1 if c != '.' else 0
                for i in range(len(rolling)):
                    tilted[y-i-adj][x] = 'O'
                rolling = []
            elif c == 'O':
                # pick up another rolling rock
                # print('picked up another')
                # print(f'Picked up rock at {y}, {x}')
                rolling.append(y)

            y+=1

    return tilted

def tiltEast(tilted):
    for y in range(len(lines[0])):
        x = 0
        rolling = []
        while x < len(lines[0]):
            c = tilted[y][x]
            if c == '#' or x == len(lines[0]) - 1:
                # put down any rocks that are rolling
                # print('stop')
                # print(f'Putting down {len(rolling)} rocks at {y}, {x}')
                for i in range(len(rolling)):
                    tilted[y][rolling[i]] = '.'
                adj = 1 if c != '.' else 0
                for i in range(len(rolling)):
                    tilted[y][x-i-adj] = 'O'
                rolling = []
            elif c == 'O':
                # pick up another rolling rock
                # print('picked up another')
                # print(f'Picked up rock at {y}, {x}')
                rolling.append(x)

            x+=1

    return tilted

def tiltWest(tilted):
    for y in range(len(lines[0])):
        x = len(lines[0]) - 1
        rolling = []
        while x >= 0 :
            c = tilted[y][x]
            if c == '#' or x == 0:
                # put down any rocks that are rolling
                # print('stop')
                # print(f'Putting down {len(rolling)} rocks at {y}, {x}')
                for i in range(len(rolling)):
                    tilted[y][rolling[i]] = '.'
                adj = 1 if c != '.' else 0
                for i in range(len(rolling)):
                    tilted[y][x+i+adj] = 'O'
                rolling = []
            elif c == 'O':
                # pick up another rolling rock
                # print('picked up another')
                # print(f'Picked up rock at {y}, {x}')
                rolling.append(x)

            x-=1

    return tilted

def part1(lines):
    # first make a mutable 2d array
    tilted = []
    for line in lines:
        tilted.append([c for c in line])

    # print(f'Pre-Tilted:\n')
    # for t in tilted:
    #     print(''.join(t))

    # Look for a repeating cycle, when we find it jump to the end assuming the cycle has
    # repeated itself enough times, and then just run the remaining loops.
    seen = {}
    iterations = 1000000000
    for i in range(iterations):
        tilted = tiltNorth(tilted)
        tilted = tiltWest(tilted)
        tilted = tiltSouth(tilted)
        tilted = tiltEast(tilted)

        tiltedString = ''
        for t in tilted:
            tiltedString = tiltedString + ''.join(t)
            print(''.join(t))
        print(f'\nTiltedString: {tiltedString}\n')
        if tiltedString in seen:
            print(f'Saw config {i} at iteration {seen[tiltedString]}')

            remaining = (iterations - i) % (i - seen[tiltedString])
            print(f'Need to loop {remaining} more times')
            for j in range(remaining - 1):
                tilted = tiltNorth(tilted)
                tilted = tiltWest(tilted)
                tilted = tiltSouth(tilted)
                tilted = tiltEast(tilted)

            break
        else:
            seen[tiltedString] = i

    # print(f'Tilted 3 cycle:\n')
    # for t in tilted:
    #     print(''.join(t))

    totalLoad = 0
    for i in range(len(tilted)):
        loadFactor = len(tilted) - i
        load = sum(map(lambda c: loadFactor if c == 'O' else 0, tilted[i]))
        totalLoad += load

    print(f'Total load: {totalLoad}')

part1(lines)
