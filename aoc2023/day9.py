import aoc_utils

testInput = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
input = aoc_utils.PuzzleInput('input-day9.txt', testInput)

lines = input.getInputLines(test=False)

def lastSequenceHasNonZeros(sequences):
    lastSequence = sequences[-1]
    return len(list(filter(lambda i: i != 0, lastSequence))) != 0

def part1(lines):
    sum = 0
    for line in lines:
        # build up the list of differences
        sequences = [aoc_utils.splitInts(line)]
        while lastSequenceHasNonZeros(sequences):
            nextSequence = []
            for i in range(len(sequences[-1]) - 1):
                nextSequence.append(sequences[-1][i+1] - sequences[-1][i])
            sequences.append(nextSequence)

        print(f'Sequences: {sequences}')

        # then work backwards to get the next number in each sequence
        # first adding a zero to the last sequence of all zeros
        sequences[-1].append(0)
        for i in range(len(sequences) - 2, -1, -1):
            sequences[i].append(sequences[i][-1] + sequences[i+1][-1])

        print(f'Updated sequences: {sequences}')
        print(f'Next value is {sequences[0][-1]}')
        sum = sum + sequences[0][-1]

    print(f'sum: {sum}')


def part2(lines):
    sum = 0
    for line in lines:
        # build up the list of differences
        sequences = [aoc_utils.splitInts(line)]
        while lastSequenceHasNonZeros(sequences):
            nextSequence = []
            for i in range(len(sequences[-1]) - 1):
                nextSequence.append(sequences[-1][i+1] - sequences[-1][i])
            sequences.append(nextSequence)

        print(f'Sequences: {sequences}')

        # then work backwards to get the next number in each sequence
        # first adding a zero to the last sequence of all zeros
        sequences[-1].append(0)
        for i in range(len(sequences) - 2, -1, -1):
            sequences[i].insert(0, sequences[i][0] - sequences[i+1][0])

        print(f'Updated sequences: {sequences}')
        print(f'Next value is {sequences[0][0]}')
        sum = sum + sequences[0][0]

    print(f'sum: {sum}')


part2(lines)