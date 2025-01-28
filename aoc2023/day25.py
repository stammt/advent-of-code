from collections import defaultdict, namedtuple
from itertools import combinations, count
import itertools
import operator
import random

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

# Deep copy the connections map so we don't corrupt the original edges
def deep_copy_connections(connections: dict[str, list[str]]):
    contracted = dict()
    for n in connections.keys():
        if len(n) > 0:
            copyc = [e for e in connections[n]]
            contracted[n] = copyc
    return contracted

def part1():
    connections = defaultdict(list)
    for line in lines:
        rhs,lhs = line.split(': ')
        lhss = lhs.split(' ')
        for l in lhss:
            connections[rhs].append(l)
            connections[l].append(rhs)
    
    # Use Karger's algorithm to reduct the graph to two contracted nodes, and then
    # see how many edges would remain between those nodes. This works randomly, so
    # repeat until we get 3.
    # https://en.wikipedia.org/wiki/Karger%27s_algorithm
    while True:
        contracted = deep_copy_connections(connections)

        while len(contracted) > 2:
            nodes = list(contracted.keys())

            # Pick a random edge u,v
            u = nodes[random.randint(0, len(nodes) - 1)]
            v = contracted[u][random.randint(0, len(contracted[u]) - 1)]

            # create a new node uv, replace any edges to u or v with an edge to uv
            uv = u+v
            edges = set(contracted[u] + contracted[v])
            edges.remove(u)
            edges.remove(v)
            contracted[uv] = list(edges)
            for e in edges:
                if u in contracted[e]:
                    contracted[e].remove(u)
                if v in contracted[e]:
                    contracted[e].remove(v)
                contracted[e].append(uv)

            # Then remove the original nodes u and v
            contracted.pop(u)
            contracted.pop(v)


        # we are successful if there are 3 edges remaining.
        # split each combined node back into it's original nodes, and check the
        # count of edges between the two groups in the original set of connections
        # There's probably a better way to track these counts as we contract the graph,
        # but this is good enough ;-)
        u, uconn = contracted.popitem()
        v, vconn = contracted.popitem()
        set1 = {u[i:i+3] for i in range(0, len(u), 3)}
        set2 = {v[i:i+3] for i in range(0, len(v), 3)}


        set_connections = sum([len([n2 for n2 in set2 if n2 in connections[n]]) for n in set1])
        if set_connections == 3:
            print(f'Can split on size {len(set1)} and {len(set2)}: {len(set1) * len(set2)}')
            return
        else:
            print(f'Unsuccessful split into {len(set1)} and {len(set2)}')

def part2():
    print('nyi')


runIt(part1, part2)


# brute force by trying every combination that is at least 1/2 the size
def brute_force(connections):
    minSize = len(connections) // 2
    nodes = set(connections.keys())
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
