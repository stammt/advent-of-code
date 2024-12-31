from operator import add, mul
import time
from aoc_utils import NE, NW, SE, SW, get_input_section, runIt, PuzzleInput, Grid, Point, all_directions, add, mul, splitInts, sub
import functools
import math
import re
from itertools import combinations
import sys


testInput = r"""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
input = PuzzleInput('input/day5.txt', testInput)

lines = input.getInputLines(test=False)
rules = list(map(lambda x: splitInts(x, '|'), get_input_section(lines, 0)))
updates = list(map(lambda x: splitInts(x, ','), get_input_section(lines, 1)))


def part1():
    c = 0
    for u in updates:
        # For all pairs of numbers in the update, make sure the reverse of that pair is not in the rules
        if (not any((b, a) in rules for (a, b) in combinations(u, 2))):
            c += u[len(u) // 2]

    print(f'sum: {c}')

def part2():
    c = 0
    def rule_lookup(m, n): return +1 if (m, n) in rules else -1 if (n, m) in rules else 0
    for u in updates:
        if (any((b, a) in rules for (a, b) in combinations(u, 2))):
            corrected = sorted(u, key=functools.cmp_to_key(rule_lookup))
            c += corrected[len(corrected) // 2]

    print(f'sum: {c}')

runIt(part1, part2)