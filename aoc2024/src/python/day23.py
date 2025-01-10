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


testInput = r"""kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

input = PuzzleInput('input/day23.txt', testInput)
lines = input.getInputLines(test=False)

def build_connections() -> dict[str, list[str]]:
    net: dict[str,list[str]] = defaultdict(list)
    for (a,b) in map(lambda line: tuple(line.split('-')), lines):
        net[a].append(b)
        net[b].append(a)
    return net

def part1():
    net = build_connections()

    # for all machines a that start with 't'
    # for each of their connections b
    # find b's connections c that are connected back to a
    # add to the result set as a sorted tuple to filter out dupes
    results = {tuple(sorted([a, b, c])) for a in filter(lambda k: k[0] == 't', net.keys())
               for b in net[a]
               for c in filter(lambda x: a in net[x], net[b])}

    print(f'Count {len(results)}')

def expand_group(a: str, group: set[str], net: dict) -> set[str]:
    for b in net[a]:
        # add b to the group if everything in the group is also connected to b
        if b not in group and group.issubset(net[b]):
            group.add(b)
            expand_group(b, group, net)            

    return group

def part2():
    net = build_connections()

    groups = {tuple(sorted(expand_group(a, {a}, net))) for a in net.keys()}

    biggest = max(groups, key=len)
    print(f'Biggest is {len(biggest)}: {biggest}')

runIt(part1, part2)
