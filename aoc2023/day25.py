from collections import defaultdict, namedtuple
from itertools import combinations, count
import itertools
import operator

import numpy
from aoc_utils import runIt, split_ints, PuzzleInput

from math import ceil, floor

testInput = r"""jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
input = PuzzleInput('input-day25.txt', testInput)


lines = input.getInputLines(test=False)


def part1():
    connections = defaultdict(set)
    for line in lines:
        rhs,lhs = line.split(': ')
        lhss = lhs.split(' ')
        for l in lhss:
            connections[rhs].add(l)
            connections[l].add(rhs)
    
    minSize = len(connections) // 2
    nodes = set(connections.keys())
    print(f'{len(nodes)} nodes, minSize {minSize}')

    for size in range(minSize, len(connections) - 3):
        print(f'Checking sets of size {size} and {len(nodes) - size}')
        for combo in itertools.combinations(nodes, size):
            set1 = set(combo)
            set2 = nodes - set1
            set_connections = 0
            for n in set1:
                set_connections += len([n2 for n2 in set2 if n2 in connections[n]])
                if set_connections > 3: break
            if set_connections == 3:
                print(f'Can split on size {size} and {len(nodes) - size}: {size * (len(nodes) - size)}')
                return
    print('nyi')

def part2():
    print('nyi')


runIt(part1, part2)