import functools
from typing import Tuple
from aoc_utils import runIt, PuzzleInput, split_ints
import math
import re
import itertools

testInput = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
input = PuzzleInput('input-day12.txt', testInput)

lines = input.getInputLines(test=False)

def apply(s, pattern) -> str:
    option = ''
    i = 0
    for c in pattern:
        if c == '?':
            option += s[i]
            i+=1
        else:
            option += c
    return option
    
def buildRegex(numbers):
    s = r'\.*'
    for i in range(len(numbers)):
        s += r'\#{' + str(numbers[i]) + '}'
        if i < len(numbers) - 1:
            s += r'[\.]+'
    s += r'\.*'
    return re.compile(s)

def matchesPattern(s: str, pattern: str) -> bool:
    for i in range(len(s)):
        if pattern[i] != '?' and s[i] != pattern[i]: return False
    return True


def blockDots(pattern: str, numbers: list[int]) -> int:
    blocks = ['#' * n for n in numbers]
    dotCount = len(pattern) - sum(numbers)# - len(blockChunks) + 1

    dotSlots = [0]
    for i in range(len(blocks)-1) : dotSlots.append(1)
    dotSlots.append(dotCount - len(blocks) + 1)

    print(f'****** checking pattern {pattern}')
    count = 0
    for s in genStr(blocks, dotSlots, pattern):
        if matchesPattern(s, pattern):
            count += 1
            # print(s)
    return count

def genStr(blocks: list[str], dotSlots: list[int], pattern: str):
    if len(blocks) == 0:
        yield ('.' * dotSlots[0])
    else:
        dotSlotsCopy = list(dotSlots)
        while dotSlotsCopy[-1] >= 0:

            prefix = ('.' * dotSlotsCopy[0]) + blocks[0]
            if matchesPattern(prefix, pattern[:len(prefix)]):
                suffixes = genStr(blocks[1:], dotSlotsCopy[1:], pattern[len(prefix):])
                    
                for s in suffixes:
                    yield prefix + s

            dotSlotsCopy[0] += 1
            dotSlotsCopy[-1] -= 1





    """
    ## ### #
    ##.###.#...
    ##.###..#..
    ##.###...#.
    ##.###....#
    ##..###.#..
    ##..###..#.
    ##..###...#
    ##...###.#.
    ##...###..#
    ##....###.#
    .##.###.#..
    .##.###..#.
    .##.###...#
    .##..###.#.
    .##..###..#
    .##...###.#
    ..##.###.#.
    ..##..###.#
    ...##.###.#

    """


def part1():
    result = 0
    for line in lines:
        [pattern, numberPattern] = line.split(' ')
        numbers = split_ints(numberPattern, ',')

        # print(f'\nCombos for\n{line}')
        lineOptions = blockDots(pattern, numbers)
        result += lineOptions

    print(f'Total: {result}')


### Copied from Norvig's python notebook after struggling with this for HOURS.
### Remember to go for the simplest solution, if it asks for a count, just
### figure out the count. Don't try all combinations!
# Still don't fully understand why caching is so effective here...
@functools.cache
def arrangements(springs: str, runs: Tuple[int]) -> int:
    """Count the number of arranagements of `springs` that is consistent with `runs`."""
    if not runs:
        return (0 if '#' in springs else 1) # One arrangement with no springs / no runs
    elif possible_damage(springs) < sum(runs):
        return 0 # Not enough damaged springs left to match runs
    else: 
        R, rest = runs[0], runs[1:]
        # Consider the case where first R characters in springs are damaged
        damaged = (0 if (possible_damage(springs[:R]) != R or springs[R:].startswith('#'))
                   else arrangements(springs[R + 1:], rest))
        # Consider the case where first character in springs is undamaged
        undamaged = (0 if springs[0] == '#' else arrangements(springs[1:], runs))
        return damaged + undamaged

def possible_damage(springs: str) -> int: 
    """The number of damaged springs ('#') plus possibly damaged springs ('?')."""
    return springs.count('#') + springs.count('?')

def part2():
    result = 0
    for line in lines:
        [pattern1, numberPattern1] = line.split(' ')
        pattern = '?'.join([pattern1, pattern1, pattern1, pattern1, pattern1])
        numberPattern = ','.join([numberPattern1, numberPattern1, numberPattern1, numberPattern1, numberPattern1])
        # print(f'{x5pattern}')
        # print(f'{x5numberPattern}')
        numbers = split_ints(numberPattern, ',')

        # lineOptions = blockDots(pattern, numbers)
        lineOptions = arrangements(pattern, tuple(numbers))

        print(f'{lineOptions} : {pattern1} - {numberPattern1} \n{pattern} {numbers}')
        print(lineOptions)
        result += lineOptions

    print(f'Total: {result}')

runIt(part1, part2)
