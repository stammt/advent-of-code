from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  A_star, manhattan_distance, splitInts, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, groupby, permutations, product
import sys
import numpy


testInput = r"""029A
980A
179A
456A
379A"""

input = PuzzleInput('input/day21.txt', testInput)
lines = input.getInputLines(test=False)

numpad = Grid([['7', '8', '9'],
               ['4', '5', '6'],
               ['1', '2', '3'],
               ['#', '0', 'A']])

dirpad = Grid([['#', '^', 'A'],
               ['<', 'v', '>']])

def dirpad_presses(p: Point, diff: Point, grid: Grid) -> list[str]:    
    dx = ''
    dy = ''
    if diff[0] != 0:
        dx = ''.join([('<' if diff[0] < 0 else '>') * abs(diff[0])])
    if diff[1] != 0:
        dy = ''.join([('^' if diff[1] < 0 else 'v') * abs(diff[1])])

    results = set()
    if grid[add(p, (diff[0], 0))] != '#':
        results.add(dx + dy + 'A')

    if grid[add(p, (0, diff[1]))] != '#':
        results.add(dy + dx + 'A')

    return list(results)

def filter_shortest(l: list[str]) -> list[str]:
    shortest_len = min(list(map(len, l)))
    results = list(filter(lambda x: len(x) == shortest_len, l))
    # print(f'returning shortest ({shortest_len}) {len(results)} out of {len(l)}')
    return results

def press_options(goals: list[str], start1: Point, g1: Grid) -> list[str]:
    p1 = start1
    results = []
    for goal in goals:
        presses = []
        for n in goal:
            # print(f'Processing {n} in {goal}')
            npos = g1.find(n)
            diff = sub(npos, p1)

            # dirpad 1
            d1goals = dirpad_presses(p1, diff, g1)
            # print(f'got goals {d1goals}')
            # print(f'd1 goal for {n} at {npos} from {pos[0]} diff {diff} is {d1goal}')
            p1 = npos

            if len(presses) == 0:
                presses = filter_shortest(d1goals)
            else:
                # print(f'updating presses')
                presses = filter_shortest([p+d for p in presses for d in d1goals])
            # print(f'presses has {len(presses)}')

        results.extend(presses)

    return results


def part1():
    complexity = 0
    for goal in lines: # ['029A']:
        l1presses = press_options([goal], (2, 3), numpad)
        # print(f'L1 {goal}: {l1presses}')

        l1shortest = sorted(l1presses, key=len)[0]
        print(f'l1shortest for {goal}: {l1shortest}')
        l2presses = press_options(l1presses, (2, 0), dirpad)
        # print(f'L2 {goal}: {l2presses}')

        l2shortest = sorted(l2presses, key=len)[0]
        print(f'l2shortest for {goal}: {l2shortest}')
        l3presses = press_options(l2presses, (2, 0), dirpad)
        # print(f'L3 {goal}: {l3presses}')

        l3shortest = sorted(l3presses, key=len)[0]
        print(f'l3shortest for {goal}: {len(l3shortest)} {l3shortest}')
        complexity += (len(l3shortest) * int(goal[:-1])) 
    print(f'total complexity: {complexity}')



def part2():
    complexity = 0
    for goal in lines: # ['029A']:
        presses = press_options([goal], (2, 3), numpad)

        for i in range(25):
            # shortest = sorted(l1presses, key=len)[0]
            # print(f'l1shortest for {goal}: {l1shortest}')
            print(f'terminal {i}')
            shortest_presses = filter_shortest(presses)
            # print(f'Shortest is {len(shortest)}: leaving {len(list(shortest_presses))} out of {len(presses)}')

            presses = press_options(shortest_presses, (2, 0), dirpad)
        # print(f'L2 {goal}: {l2presses}')

        # l2shortest = sorted(l2presses, key=len)[0]
        # print(f'l2shortest for {goal}: {l2shortest}')
        # l3presses = press_options(l2presses, (2, 0), dirpad)
        # print(f'L3 {goal}: {l3presses}')

        l3shortest = sorted(presses, key=len)[0]
        print(f'l3shortest for {goal}: {len(l3shortest)} {l3shortest}')
        complexity += (len(l3shortest) * int(goal[:-1])) 
    print(f'total complexity: {complexity}')


runIt(part1, part2)
