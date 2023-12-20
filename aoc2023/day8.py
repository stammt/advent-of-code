import aoc_utils
import numpy

testInput = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
input = aoc_utils.PuzzleInput('input-day8.txt', testInput)

lines = input.getInputLines(test=False)

def endsWithZ(addresses):
    return len(list(filter(lambda a: a[-1] == 'Z', addresses)))

def part1(lines):
    directions = lines[0]

    # Dict of node name -> tuple of left, right destinations
    desertMap = {}
    for i in range(2, len(lines)):
        name = lines[i].split()[0]
        left = lines[i][7:10]
        right = lines[i][12:15]
        desertMap[name] = (left, right)

    # print(f'map: {desertMap}')
    address = 'AAA'
    directionIndex = 0
    steps = 0
    while address != 'ZZZ':
        paths = desertMap[address]
        direction = directions[directionIndex]
        next = paths[0] if direction == 'L' else paths[1]
        # print(f'Moved {direction} from {address} to {next}')
        address = next
        directionIndex = (directionIndex + 1) % len(directions)
        steps = steps + 1

    print(f'took {steps} steps')

def part2(lines):
    directions = lines[0]

    # Dict of node name -> tuple of left, right destinations
    desertMap = {}
    addresses = []
    for i in range(2, len(lines)):
        name = lines[i].split()[0]
        left = lines[i][7:10]
        right = lines[i][12:15]
        desertMap[name] = (left, right)
        if name[-1] == 'A':
            addresses.append(name)

    print(f'taking paths from {addresses}')

    # Find the number of steps from each starting address to a node ending in 'Z',
    # then find the least common multiple of those counts
    counts = []
    for address in addresses:
        directionIndex = 0
        steps = 0
        while address[-1] != 'Z':
            paths = desertMap[address]
            direction = directions[directionIndex]
            next = paths[0] if direction == 'L' else paths[1]
            # print(f'Moved {direction} from {address} to {next}')
            address = next
            directionIndex = (directionIndex + 1) % len(directions)
            steps = steps + 1
        counts.append(steps)

    print(f'Found counts: {counts}')
    result = numpy.lcm.reduce(counts)
    print(f'Result: {result}')

part2(lines)