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

lines = input.getInputLines(test=True)

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

def is_potential(s: str, numbers: list[int], hashCount: int) -> bool:
    if s.count('#') > hashCount:
        return False
    
    slot = s.find('?')
    if slot != -1:
        # print(f'Trimming {s} to {s[0:slot]}')
        s = s[0:slot]


    blockLen = 0
    blocks = []
    for sidx in range(len(s)):
        if s[sidx] == '#':
            blockLen += 1
        elif blockLen > 0:
            blocks.append(blockLen)
            blockLen = 0
    if blockLen > 0:
        blocks.append(blockLen)

    # print(f'Found {blocks} in {s}')
    # if there are too many blocks, return false
    if len(blocks) > len(numbers):
        return False
    
    # if the blocks don't match, return false
    for i in range(len(blocks)):
        if blocks[i] > numbers[i]:
            return False
            
    return True


def solve(pattern: str, numbers: list[int]) -> int:
    regex = buildRegex(numbers)
    hashCount = sum(numbers)
    q = [pattern]
    result = 0
    print(f'Solve {pattern}')
    while len(q) != 0:
        s = q.pop(0)
        firstSlot = s.find('?')
        if firstSlot == -1:
            match_result = regex.fullmatch(s)
            if match_result != None:
                result += 1
        else:
            opt1 = s[0:firstSlot] + '.' + s[firstSlot+1:]
            if is_potential(opt1, numbers, hashCount):
                q.append(opt1)
            opt2 = s[0:firstSlot] + '#' + s[firstSlot+1:]
            if is_potential(opt2, numbers, hashCount):
                q.append(opt2)
            # print(q)
    return result

def part1():
    result = 0
    for line in lines:
        [pattern, numberPattern] = line.split(' ')
        numbers = split_ints(numberPattern, ',')
        optionCount = solve(pattern, numbers)
        print(f'Fount {optionCount} for {line}')
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

        optionCount = solve(pattern, numbers)
        print(f'Found {optionCount} for {line}')
        result += optionCount

    print(f'Total: {result}')

runIt(part1, part2)
