import aoc_utils
import numpy

testInput = """Time:      7  15   30
Distance:  9  40  200"""
input = aoc_utils.PuzzleInput('input-day6.txt', testInput)

lines = input.getInputLines(test=False)

def part2(lines):
    time = int(''.join(lines[0].split(':')[1].strip().split()))
    distance = int(''.join(lines[1].split(':')[1].strip().split()))

    # Iterate until we have a winning time, then the number of ways to win will
    # be the total time - (2 * the speed)
    # Optimization would be to do a binary search from 0 - (t/2) to find the lowest winning
    # time, but didn't need to do that.
    for t in range(time):
        if (t * (time - t) > distance):
            waysToWin = time - (2 * t) + 1 # starting at zero
            print(f'ways: {waysToWin}: started winning with speed {t} to {time - t}')
            return
    print('Could not win?')


def part1(lines):
    times = aoc_utils.splitInts(lines[0].split(':')[1].strip())
    distances = aoc_utils.splitInts(lines[1].split(':')[1].strip())

    races = [(times[i], distances[i]) for i in range(len(times))]

    waysToWin = []
    for race in races:
        results = []
        for t in range(race[0]):
            speed = t
            timeTraveled = race[0] - t
            distance = speed * timeTraveled
            if (distance > race[1]):
                results.append(distance)
        waysToWin.append(len(results))

    product = numpy.prod(waysToWin)
    print(f'product: {product} from {waysToWin}')


part2(lines)