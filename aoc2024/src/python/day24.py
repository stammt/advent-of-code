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
                    inputs[k] = a & b
                elif gate[1] == 'OR':
                    inputs[k] = a | b
                elif gate[1] == 'XOR':
                    inputs[k] = a ^ b
                gates.pop(k)

    zees = ''.join(map(lambda x: str(inputs[x]), reversed(sorted([k for k in inputs.keys() if k.startswith('z')]))))
    print(zees)
    zd = int(zees, 2)
    print(zd)

def get_swapped_output(a, op, b, gate_lookups, swaps):
    key = (a, op, b)
    result = 'NOPE'
    if key in gate_lookups:
        result = gate_lookups[key]
    else:
        key = (b, op, a)
        if key in gate_lookups:
            result = gate_lookups[key]
    if result != 'NOPE' and result in swaps:
        print(f'swapping result {result} for {swaps[result]}')
        result = swaps[result]
    return result

def diagnose(gates, swaps):
    # adders https://en.wikipedia.org/wiki/Adder_(electronics)
    # 1 bit full adder (https://en.wikipedia.org/wiki/File:Full-adder_logic_diagram.svg)
    # Inputs a,b,c (in)
    # a XOR b -> w
    # a AND B -> z
    # w XOR c -> S
    # w AND c -> y
    # y OR z  -> c (out)
    # Ripple-carry multibit adder chains 1 bit full adders, where c (out) goes to c (in) of the next bit

    inputs = {
        'a': 0,
        'b': 1,
        'c': 1
    }
    one_bit_full_adder_gates = {
        'a': ('x', 'XOR', 'y'),
        'b': ('x', 'AND', 'y'),
        'c': ('a', 'AND', 'carry_in'),
        'S': ('b', 'XOR', 'carry_in'), # output
        'C': ('c', 'OR', 'b') # carry_out
    }
    one_bit_half_adder_gates = {
        'S': ('a', 'XOR', 'b'),
        'C': ('a', 'AND', 'b')
    }

    # z45 is carry bit from last full adder kbm OR spc
    # z44 output from last full adder hhg XOR hhp
    # ...
    # z01 is output from first full adder, mcg is carry in, mcg XOR vcn; x01 XOR y01 -> vcn
    # z00 is output from first half adder y00 XOR x00, carry  mcg x00 AND y00

    # reverse lookup, we know the gate, what's the output?
    gate_lookups = {b:a for a,b in gates.items()}

    def get_output(a, op, b):
        return get_swapped_output(a, op, b, gate_lookups, swaps)
    
    # manually verified x00/y00 half adder with output carry mcg
    # run through the rest until we NOPE out, and print diagnostics
    # manually figure out the swap and add to map, then run again!
    carry = 'mcg'
    for i in range(1,45):
        carry_in = carry
        x = 'x{:02d}'.format(i)
        y = 'y{:02d}'.format(i)
        z = 'z{:02d}'.format(i)

        # built the adder and see if anything nope's out
        a = get_output(x, 'XOR', y)
        b = get_output(x, 'AND', y)
        c = get_output(a, 'AND', carry_in)
        output = get_output(a, 'XOR', carry_in)
        carry = get_output(c, 'OR', b)

        print(f'Gate {i}: output is {output}, carry is {carry}')
        if output == 'NOPE' or not output.startswith('z'):
            print(f'a is {a} -> {x} XOR {y}')
            print(f'b is {b} -> {x} AND {y}')
            print(f'c is {c} -> {a} AND {carry_in}')
            print(f'output is {output} -> {a} XOR {carry_in}')
            print(f'carry is {carry} -> {c} OR {b}')
            break



def part2():
    splits = split_on_empty_lines(lines)
    inputs = {a:int(b) for a,b in [line.split(': ') for line in splits[0]] }
    gates = {b:tuple(a.split(' ')) for (a,b) in [line.split(' -> ') for line in splits[1]] }

    swaps = {
        'shh':'z21',
        # 'z21':'shh',
        'vgs':'dtk',
        # 'dtk':'vgs',
        'dqr':'z33',
        # 'z33':'dqr',
        'pfw':'z39',
        # 'z39':'pfw'
    }

    xs = ''.join(map(lambda x: str(inputs[x]), reversed(sorted([k for k in inputs.keys() if k.startswith('x')]))))
    print(f'X={int(xs, 2)} ({xs})')

    ys = ''.join(map(lambda x: str(inputs[x]), reversed(sorted([k for k in inputs.keys() if k.startswith('y')]))))
    print(f'Y={int(ys, 2)} ({ys})')

    for a,b in swaps.items():
        gates[a], gates[b] = gates[b], gates[a]

    while len(gates) > 0:
        keys = list(gates.keys())
        for k in keys:
            gate = gates[k]
            if gate[0] in inputs and gate[2] in inputs:
                a = inputs[gate[0]]
                b = inputs[gate[2]]
                if gate[1] == 'AND':
                    inputs[k] = a & b
                elif gate[1] == 'OR':
                    inputs[k] = a | b
                elif gate[1] == 'XOR':
                    inputs[k] = a ^ b
                gates.pop(k)

    zees = ''.join(map(lambda x: str(inputs[x]), reversed(sorted([k for k in inputs.keys() if k.startswith('z')]))))
    print(f'Z={int(zees, 2)} ({zees}) should be X+Y={int(xs, 2) + int(ys, 2)}')

    all_swaps = list(swaps.keys()) + list(swaps.values())
    print(f'Swaps: {','.join(sorted(all_swaps))}')


runIt(part1, part2)
