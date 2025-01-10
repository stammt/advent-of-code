from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  A_star, sliding_window, splitInts, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, groupby, permutations, product
import sys
import numpy


testInput = r"""1
2
3
2024"""

input = PuzzleInput('input/day22.txt', testInput)
lines = input.getInputLines(test=False)


def next_secret(secret: int) -> int:
    secret ^= (secret *   64) % 16777216
    secret ^= (secret //  32) % 16777216
    secret ^= (secret * 2048) % 16777216
    return secret

def part1():
    sum = 0
    for line in lines:
        secret = int(line)
        for i in range(2000):
            secret = next_secret(secret)
        sum += secret
    print(f'sum: {sum}')

def part2():
    sequence_to_prices: dict[tuple[int], int] = defaultdict(int)

    for line in lines:
        secrets = [int(line)]
        for i in range(2000):
            secrets.append(next_secret(secrets[i]))
        prices = list(map(lambda x: x%10, secrets))
        price_diffs = [prices[i] - prices[i-1] for i in range(1, 2001)]
        seen_seqs = set()
        for i in range(3, 2000):
            seq = tuple(price_diffs[i-3:i+1])
            if seq not in seen_seqs:
                sequence_to_prices[seq] += prices[i+1]
                seen_seqs.add(seq)

    best_sequence_price = max(sequence_to_prices.values())
    print(f'Best price {best_sequence_price}')

runIt(part1, part2)
