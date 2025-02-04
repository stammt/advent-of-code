from aoc_utils import runIt

min_val = 145852
max_val = 616942

def is_valid(val: list[int], part1: bool) -> bool:
    # must have a doubled number
    found_double = False
    if (part1):
        for i in range(len(val) - 1):
            if val[i+1] == val[i]:
                found_double = True
                break
    else:
        for i in range(len(val) - 1):
            # only count this double if it's at the beginning or end, or not part of a larger string of the same value
            if val[i+1] == val[i] and (i == len(val) - 2 or val[i+2] != val[i]) and (i == 0 or val[i-1] != val[i]):
                found_double = True
                break
    if not found_double: return False

    i = int(''.join(map(str, val)))
    return i >= min_val and i <= max_val

# Recursively buid the list of ints, each successive int starting higher than the previous to ensure no decreasing numbers
def generate(val: list[int], part1: bool) -> int:
    if len(val) == 6:
        return 1 if is_valid(val, part1) else 0
    
    start = 0 if len(val) == 0 else val[-1]
    return sum(generate(val + [i], part1) for i in range(start, 10))

def part1():
    count = generate([], part1=True)
    print(f'Passwords: {count}')

def part2():
    count = generate([], part1=False)
    print(f'Part 2 Passwords: {count}')

runIt(part1, part2)