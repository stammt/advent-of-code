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


def mix(secret: int, value: int) -> int:
    return secret ^ value

def prune(secret: int) -> int:
    return secret % 16777216

def next_secret(secret: int) -> int:
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
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
    all_prices = []
    testseq = (-2,2,-1,-1)

    sequence_to_prices: dict[tuple[int], int] = defaultdict(int)
    best_sequence = tuple()
    best_sequence_price = -1

    for line in lines:
        secret = int(line)
        prices = [secret%10]
        price_diffs = []
        seen_seqs = set()
        for i in range(2000):
            secret = next_secret(secret)
            prices.append(secret%10)
            price_diffs.append(prices[i+1] - prices[i])
            if i >= 3:
                seq = (price_diffs[i-3], price_diffs[i-2], price_diffs[i-1], price_diffs[i])
                if seq not in seen_seqs:
                    sequence_to_prices[seq] += prices[i+1]
                    if sequence_to_prices[seq] > best_sequence_price:
                        best_sequence_price = sequence_to_prices[seq]
                        best_sequence = seq
                    seen_seqs.add(seq)
        all_prices.append(prices)

    # for k,v in sequence_to_prices.items():
    #     if v > best_sequence_price:
    #         print(f'Found new best {k} for price {v}')
    #         best_sequence = k
    #         best_sequence_price = v
    
    print(f'Best price {best_sequence_price} from {best_sequence}')

runIt(part1, part2)
