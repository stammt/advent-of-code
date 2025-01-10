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


testInput = r"""x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

testInput2 = r"""x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

input = PuzzleInput('input/day24.txt', testInput2)
lines = input.getInputLines(test=False)


def part1():
    splits = split_on_empty_lines(lines)
    inputs = {a:int(b) for a,b in [line.split(': ') for line in splits[0]] }
    gates = {b:tuple(a.split(' ')) for (a,b) in [line.split(' -> ') for line in splits[1]] }

    while len(gates) > 0:
        keys = list(gates.keys())
        for k in keys:
            gate = gates[k]
            if gate[0] in inputs and gate[2] in inputs:
                a = inputs[gate[0]]
                b = inputs[gate[2]]
                if gate[1] == 'AND':
                    inputs[k] = 1 if a == 1 and b == 1 else 0
                elif gate[1] == 'OR':
                    inputs[k] = 1 if a == 1 or b == 1 else 0
                elif gate[1] == 'XOR':
                    inputs[k] = 1 if a != b else 0
                gates.pop(k)

    zees = ''.join(map(lambda x: str(inputs[x]), reversed(sorted([k for k in inputs.keys() if k.startswith('z')]))))
    print(zees)
    zd = int(zees, 2)
    print(zd)



def part2():
    print('nyi')


runIt(part1, part2)
