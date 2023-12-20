import aoc_utils
import math
import re
import itertools

testInputx = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
testInputx = """?###???????? 3,2,1"""
testInputx = """?.???#??.#?? 4,1,2"""
testInputx = """#####?.????#???# 5,1,1,3"""
testInputx = """.??..??...?##. 1,1,3"""
testInput = """#.?#.#???????...??## 1,2,2,1,1,4"""
input = aoc_utils.PuzzleInput('input-day12.txt', testInput)

lines = input.getInputLines(test=True)

def buildRegex(pattern):
    # start with any number of '.'
    regexStr = '^\.*'

    spanLengths = pattern.split(',')
    for i in range(len(spanLengths)):
        regexStr = regexStr + '\#{' + spanLengths[i] + '}'

        # add at least one '.' between groups
        if (i < len(spanLengths) - 1):
            regexStr = regexStr + "\.+"

    # end with any number of '.'
    regexStr = regexStr + '\.*$'
    return regexStr

def bruteForce(s, pattern):
    indices = [i for i, ltr in enumerate(s) if ltr == '?']
    print(f'indices {indices}')
    combos = itertools.product('#.', repeat=len(indices))
    # print(f'combos: {len(combos)}')
    hashCount = sum(list(map(lambda c: int(c), pattern.split(','))))
    results = []
    for combo in combos:
        result = ''
        comboIndex = 0
        for i in range(len(s)):
            if s[i] == '?':
                result += combo[comboIndex]
                comboIndex += 1
            else:
                result += s[i]
        # drop results without enough # chars
        if (result.count('#') == hashCount):
            results.append(result)
    return results

def bruteForce2(s, pattern):
    indices = [i for i, ltr in enumerate(s) if ltr == '?']
    print(f'indices {indices}')
    combos = itertools.product('#.', repeat=len(indices))
    # print(f'combos: {len(combos)}')
    patternCounts = list(map(lambda c: int(c), pattern.split(',')))
    results = []
    for combo in combos:
        result = []
        match = True
        comboIndex = 0
        lastChar = '.'
        patternIndex = 0
        hashCount = 0
        # print(f'Trying combo: {combo}')
        for i in range(len(s)):
            ch = s[i]
            if ch == '?':
                ch = combo[comboIndex]
                comboIndex += 1
            result += ch
            if ch == '#':
                # count the hash in the current pattern, break if there are too many
                hashCount += 1
                if patternIndex == len(patternCounts):
                    match = False
                    # print(f'Found a hash after the last pattern {patternIndex}: {result}')
                    break
                if hashCount > patternCounts[patternIndex]:
                    match = False
                    # print(f'Too many hashes at pattern {patternIndex}: {result}')
                    break
            elif ch == '.' and lastChar != '.':
                # end the current pattern and break if we haven't gotten enough hashes
                if hashCount < patternCounts[patternIndex]:
                    match = False
                    # print(f'Not enough hashes at pattern {patternIndex}: {result}')
                    break
                if (hashCount > 0):
                    patternIndex += 1
                    # # ran out of patterns to match
                    # if patternIndex == len(patternCounts):
                    #     match = False
                    #     print(f'Ran out of patterns to match {result}')
                    #     break
                    hashCount = 0
            lastChar = ch

        # end of the string, see if we've matched the last pattern
        if lastChar == '#':
            if hashCount < patternCounts[patternIndex]:
                # print(f'Not enough hashes at end {patternIndex}: {result}')
                match = False

            patternIndex += 1

        if patternIndex != len(patternCounts):
            # print(f'Did not match all patterns {patternIndex}: {result} ')
            match = False
                
        if match == True:
            # print(f'MATCH: {''.join(result)}')
            results.append(result)
    return results


def findCandidatePosition(s, sStart, hashCount):
    if (sStart >= len(s)):
        # print(f'Hit the end')
        return None
    
    lastChar = '.' if sStart == 0 else s[sStart - 1]
    # print(f'Placing {hashCount} in {s} starting at {sStart}')
    # for i in range(sStart, len(s)):
    i = sStart
    if lastChar != '#' and s[i] != '.':
        valid = True
        for h in range(hashCount):
            # if we hit a '.', it can't fit
            if (i+h) < len(s) and s[i + h] == '.':
                valid = False
            # if we hit the end of the string, it can't fit
            if (i+h) >= len(s)-1 and h < hashCount - 1:
                valid = False
        # if there's another '#' in the string, it would be too long
        if (i+h+1) < len(s) and s[i+h+1] == '#':
            valid = False
        if valid:
            # print(f'First pattern of {hashCount} can fit at position {i}')
            return i
    return None

def buildString(positions, hashCounts, length):
    result = []
    positionIndex = 0
    # print(f'Building string from {positions}, {hashCounts}, {length}')
    while len(result) < length:
        if (positionIndex < len(positions) and len(result) == positions[positionIndex]):
            for x in range(hashCounts[positionIndex]):
                result.append('#')
            positionIndex += 1
        else:
            result.append('.')
    return ''.join(result)

def findStartingPositions(s, sStart, remainingTargets, previousPositions=[]):
    positions = []
    print(f'***findStartinPositions({s}, {sStart}, {remainingTargets}, {previousPositions})')
    for i in range(sStart, len(s)):
        pos = findCandidatePosition(s, i, remainingTargets[0])
        if (pos != None):
            nextPrev = (previousPositions + [pos])
            # print(f'Building on {nextPrev}')
            if len(remainingTargets) > 1:
                nextPositions = findStartingPositions(s, pos + remainingTargets[0] + 1, remainingTargets[1:], nextPrev)
                if (nextPositions != None):
                    positions += nextPositions
            else:
                positions += [nextPrev]
    return None if len(positions) == 0 else positions

def doubleCheck(s, built):
    if len(s) != len(built):
        print(f'Lengths do not match!\n{s}\n{built}')
        return False

    for i in range(len(s)):
        if s[i] != '?' and s[i] != built[i]:
            print(f'Strings do not match:\n{s}\n{built}')
            return False
        
    return True

def smarter(s, pattern, regexPattern):
    hashCounts = list(map(lambda c: int(c), pattern.split(',')))
    positions = findStartingPositions(s, 0, hashCounts)
    count = 0
    for p in positions:
        built = buildString(p, hashCounts, len(s))
        m = re.search(regexPattern, built)
        if m == None:
            print(f'\nStarting positions: {len(positions)} {positions}')
            print(f'For {s}: {pattern}')
            print(f'!!! does not match regex: {built}')
        check = doubleCheck(s, built)
        if (check == False):
            print(f'For {s} - {pattern}')
        else:
            count += 1

    return count


def part1(lines):
    sum = 0
    for line in lines:
        count = 0
        s, pattern = line.split()
        regexPattern = buildRegex(pattern)
        # print(f'\n{s} -- {pattern} -- {regexPattern}')
        count = smarter(s, pattern, regexPattern)
        sum += count

    print(f'Total: {sum}')

def part2(lines):
    sum = 0
    for line in lines:
        foldedString, foldedPattern = line.split()
        unfoldedString = foldedString
        unfoldedPattern = foldedPattern
        for i in range(4):
            unfoldedString = unfoldedString + '?' + foldedString
            unfoldedPattern = unfoldedPattern + ',' + foldedPattern
        
        print(f'Unfolded: {unfoldedString} - {unfoldedPattern}')

        count = 0
        s = unfoldedString
        pattern = unfoldedPattern
        # s, pattern = line.split()
        regexPattern = buildRegex(pattern)
        # print(f'\n{s} -- {pattern} -- {regexPattern}')
        count = smarter(s, pattern, regexPattern)
        print(f'So far sum is {sum}')
        sum += count

    print(f'Total: {sum}')

part2(lines)