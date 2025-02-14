from collections import defaultdict
import sys
from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance
from itertools import count
from numpy import arctan, arctan2, pi
import math

testInput1 = r"""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""
testInput2 = r"""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""
testInput = r"""157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
input = PuzzleInput('input/day14.txt', testInput2)

lines = input.getInputLines(test=True)

class Reaction:
    def __init__(self, line):
        parts = line.split(' => ')
        self.output_count = int(parts[1].split(' ')[0])
        self.output_type = parts[1].split(' ')[1]

        input_parts = parts[0].split(', ')
        self.inputs = dict()
        for i in input_parts:
            self.inputs[i.split(' ')[1]] = int(i.split(' ')[0])

    def can_run(self, resources: dict[str, int]) -> bool:
        for k, v in self.inputs.items():
            if resources[k] < v:
                return False
        return True
    
    def react(self, resources: dict[str, int]):
        for k, v in self.inputs.items():
            resources[k] -= v

    def __str__(self):
        return f'{self.output_count} {self.output_type}'


def solve(target_type: str, target_count: int, resources: dict[str, int], reactions: list[Reaction]):
    target_reaction = [r for r in reactions if r.output_type == target_type][0]
    print(f'Need {target_count} {target_type}')

    for k, v in target_reaction.inputs.items():
        input_reaction = [r for r in reactions if r.output_type == k][0]
        if 'ORE' in input_reaction.inputs:
            print(f'Adding {k}: {target_count} * {v} = {(target_count * v)}')
            resources[k] += target_count * v
        else:
            solve(k, v * target_count, resources, reactions)


def part1():
    reactions = [Reaction(line) for line in lines]
    # fi = [r for r in reactions if r.output_type == 'FUEL'][0]

    resources = defaultdict(int)
    solve('FUEL', 1, resources, reactions)
    print(resources)
    ore = 0
    for k,v in resources.items():
        ore_reaction = [r for r in reactions if r.output_type == k and 'ORE' in r.inputs][0]
        times = math.ceil(v / ore_reaction.output_count)
        cost = ore_reaction.inputs['ORE'] * times
        print(f'{cost} for {v} {k} times {times}')
        ore += cost
    print(ore)

def part2():
    print('nyi')

runIt(part1, part2)