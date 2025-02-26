from collections import defaultdict
import sys
from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance
from itertools import count
from numpy import arctan, arctan2, pi
import math

# 0 1 2 3 4 5 6 7 8 9
# 0 . . . . . . 1 . .
# . . . . 2 . . . . .
# . 3 . . . . . . 4 .
# . . . . . 5 . . . .
# . . 6 . . . . . . 7
# . . . . . . 8 . . .
# . . . 9
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

lines = input.getInputLines(test=True)

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

# what position was the card at pos at, before this deal
def reverse_deal_with_increment(inc: int, pos: int, deck_size: int) -> int:
    i = 0 # where we're dealing from
    deal = 0 # where we're dealing to
    while i < deck_size:
        here = (pos - deal) % inc == 0
        # print(f'Dealing from {i} to {deal} {here}')
        if here:
            # while deal< pos:
            #     i+= 1
            #     deal += inc
            return i + ((pos - deal) // inc)
        c = (deck_size - deal) // inc
        i += c + 1
        deal = (deal + inc * (c+1)) % deck_size
        # print(f'Dealt {c} cards, next i {i} next deal {deal}')
    print(f'reverse deal failed')
    return -1
        

def reverse_deal_into_new_stack(pos: int, deck_size: int) -> int:
    return deck_size - pos - 1

def reverse_cut(pos: int, n: int, deck_size: int) -> int:
    if n >= 0:
        if pos >= deck_size - n:
            return pos - (deck_size - n)
        else:
            return pos + n
    else:
        if pos < abs(n):
            return pos + (deck_size - abs(n))
        else:
            return pos - abs(n)

def part1():
    deck = [i for i in range(10)]
    print(deck)
    for line in lines:
        if line.startswith('deal with increment'):
            inc = int(line[len('deal with increment '):])
            deck = deal_with_increment(inc, deck)
        elif line.startswith('deal into new stack'):
            deck = deal_into_new_stack(deck)
        elif line.startswith('cut'):
            n = int(line[len('cut '):])
            deck = cut(n, deck)
        print(line)
        print(deck)
    # print(deck.index(2019))

def part2():
    # deck = [i for i in range(119315717514047)]
    shuffle_times = 101741582076661
    #           113051296978736
    deck_size = 119315717514047
    lines.reverse()
    pos = 2020
    seen = set()

    for i in range(shuffle_times):
        for line in lines:
            if line.startswith('deal with increment'):
                inc = int(line[len('deal with increment '):])
                pos = reverse_deal_with_increment(inc, pos, deck_size)
            elif line.startswith('deal into new stack'):
                pos = reverse_deal_into_new_stack(pos, deck_size)
            elif line.startswith('cut'):
                n = int(line[len('cut '):])
                pos = reverse_cut(pos, n, deck_size)
            # print(f'Pos {pos} after {line}')
        if pos in seen:
            print(f'repeated {pos} at {i}')
            break
        seen.add(pos)
        # print(f'{i} : {pos}')
        if pos == 2020:
            print(f'Back to 2020 at {i}')
            break

    # 11378516720869 too low
    print(pos)

runIt(part1, part2)