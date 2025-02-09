from collections import defaultdict
import aoc_utils
from itertools import count
import intcode

testInput = r"""109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"""
input = aoc_utils.PuzzleInput('input/day09.txt', testInput)

lines = input.getInputLines(test=False)

def part1():
    ints = list(aoc_utils.splitInts(lines[0], ','))
    # ints = [104,1125899906842624,99] # outputs the number in the middle
    # ints = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99] # outputs a copy of itself
    # ints = [1102,34915192,34915192,7,4,7,99,0] # outputs a 16 digit number
    memory = defaultdict(int)
    for i in range(len(ints)):
        memory[i] = ints[i]
    output, state, i, rb = intcode.run_intcode(memory, [1])
    print(output)

def part2():
    ints = list(aoc_utils.splitInts(lines[0], ','))
    memory = defaultdict(int)
    for i in range(len(ints)):
        memory[i] = ints[i]
    output, state, i, rb = intcode.run_intcode(memory, [2])
    print(output)

aoc_utils.runIt(part1, part2)