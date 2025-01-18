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

def part1():
    result = 0
    for line in lines:
        [pattern, numberPattern] = line.split(' ')
        numbers = split_ints(numberPattern, ',')
        hashCount = sum(numbers) - pattern.count('#')
        slots = pattern.count('?')
        optionCount = 0
        regex = buildRegex(numbers)
        for s in itertools.product('#.', repeat=slots):
            if s.count('#') != hashCount:
                continue
            option = apply(s, pattern)
            match_result = regex.fullmatch(option)
            if match_result != None:
                optionCount += 1
        # print(f'Fount {optionCount} for {line}')
        result += optionCount

    print(f'Total: {result}')

def part2():
    result = 0
    for line in lines:
        [pattern, numberPattern] = line.split(' ')
        pattern = pattern * 5
        numberPattern = ','.join([numberPattern, numberPattern, numberPattern, numberPattern, numberPattern])
        # print(f'{x5pattern}')
        # print(f'{x5numberPattern}')
        numbers = split_ints(numberPattern, ',')
        slots = pattern.count('?')
        hashCount = sum(numbers) - pattern.count('#')
        optionCount = 0
        regex = buildRegex(numbers)
        for s in itertools.product('#.', repeat=slots):
            if s.count('#') != hashCount:
                continue

            # print(f'checking {s}')
            option = apply(s, pattern)
            # print(f'checking {s} against {option}')
            match_result = regex.fullmatch(option)
            if match_result != None:
                optionCount += 1
        print(f'Fount {optionCount} for {line}')
        result += optionCount

    print(f'Total: {result}')

runIt(part1, part2)
