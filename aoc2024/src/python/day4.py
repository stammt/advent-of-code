from operator import add, mul
import time
from aoc_utils import NE, NW, SE, SW, runIt, PuzzleInput, Grid, Point, all_directions, add, mul, sub
import functools
import math
import re
import itertools
import sys


testInput = r"""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
input = PuzzleInput('input/day4.txt', testInput)

lines = input.getInputLines(test=False)
grid = Grid(lines)

def check_word(word:str, pos:Point, dir) -> bool:
    return all(grid.get(add(pos, mul(dir, i))) == ch for i, ch in enumerate(word))

def find(word:str, pos:Point, dirs) -> int:
    if (grid.get(pos) == word[0]):
        return sum(check_word(word, pos, d) for d in dirs) 
    return 0

def part1():
    c = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            c += find('XMAS', (x, y), all_directions)

    print(f'sum {c}')

def part2():
    c = 0
    diagonal_pairs = ([SE, NE], [SW, NW],  [SE, SW], [NE, NW])
    aPoints = grid.findAll('A')
    for a in aPoints:
        for d1, d2 in diagonal_pairs:
            if (check_word('MAS', sub(a, d1), d1) and check_word('MAS', sub(a, d2), d2)):
                c+=1

    print(f'sum {c}')

runIt(part1, part2)