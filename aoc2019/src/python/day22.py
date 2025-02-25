from collections import defaultdict
import sys
from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance
from itertools import count
from numpy import arctan, arctan2, pi
import math

# 0 3 6 9 2 5 8 1 4 7
testInput1 = r"""deal with increment 7
deal into new stack
deal into new stack"""

# 6 3 0 7 4 1 8 5 2 9
testInput2 = r"""deal with increment 7
deal with increment 9
cut -2"""

# 9 2 5 8 1 4 7 0 3 6
testInput3 = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""
input = PuzzleInput('input/day22.txt', testInput3)

lines = input.getInputLines(test=False)

def deal_with_increment(inc: int, deck: list[int]) -> list[int]:
    result = [0 for i in range(len(deck))]
    deal = 0
    for pos in range(len(deck)):
        result[deal] = deck[pos]
        deal = (deal + inc) % len(deck)
    return result

def deal_into_new_stack(deck: list[int]) -> list[int]:
    deck.reverse()
    return deck

def cut(n: int, deck: list[int]) -> list[int]:
    return deck[n:len(deck)] + deck[0:n]

def part1():
    deck = [i for i in range(10007)]
    for line in lines:
        if line.startswith('deal with increment'):
            inc = int(line[len('deal with increment '):])
            deck = deal_with_increment(inc, deck)
        elif line.startswith('deal into new stack'):
            deck = deal_into_new_stack(deck)
        elif line.startswith('cut'):
            n = int(line[len('cut '):])
            deck = cut(n, deck)
    print(deck.index(2019))

def part2():
    print('nyi')

runIt(part1, part2)