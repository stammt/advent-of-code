from collections import defaultdict
import sys
from aoc_utils import PuzzleInput, runIt, Point, manhattan_distance
from itertools import count
from numpy import arctan, arctan2, pi
import math

# 31
testInput1 = r"""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

# 165
testInput2 = r"""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""

# 13312
testInput3 = r"""157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

# 180697
testInput4 = r"""2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

# 2210736
testInput5 = r"""171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""
input = PuzzleInput('input/day14.txt', testInput5)

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


def solve(target_type: str, target_count: int, resources: dict[str, int], reactions: list[Reaction]) -> int:
    target_reaction = [r for r in reactions if r.output_type == target_type][0]

    # print(f'Looking for {target_count} {target_type} already have {resources[target_type]}')

    # If we have enough already, use it
    if resources[target_type] >= target_count:
        resources[target_type] -= target_count
        # print(f'Already had enough, now have {resources[target_type]} left')
        return 0
    
    # If this can be made with ore, make it
    elif 'ORE' in target_reaction.inputs:
        # how much do we need after taking into account what we have
        need = target_count - resources[target_type]

        # how many purchases do we need to make to get what we need
        times = math.ceil(need / target_reaction.output_count)

        resources[target_type] += (target_reaction.output_count * times) - target_count
        ore = (target_reaction.inputs['ORE'] * times)

        # print(f'Spent {ore} ({target_reaction.inputs['ORE']} x {times}) on {target_reaction.output_count * times} {target_type} have {resources[target_type]} remaining')
        return ore

    # Sum the cost of making the components - figure out how many reactions we need based on what we need and how much
    # we already have of the target type, then the results of the reactions minus what we need to the leftover resources
    else:
        cost = 0
        reaction_count = math.ceil((target_count - resources[target_type]) / target_reaction.output_count)
        # print(f'Need to run {target_reaction} {reaction_count} times to get {reaction_count * target_reaction.output_count}')
        for k, v in target_reaction.inputs.items():
            cost += solve(k, v * reaction_count, resources, reactions)
        resources[target_type] += (reaction_count * target_reaction.output_count) - target_count
        # print(f'Done building {target_count} {target_type} for {cost} still have {resources[target_type]}\n')

        return cost

def part1():
    reactions = [Reaction(line) for line in lines]
    ore = solve('FUEL', 1, defaultdict(int), reactions)
    print(ore)

def part2():
    reactions = [Reaction(line) for line in lines]

    # Keep spending ore to produce fuel and see when we have enough to produce a fuel unit without spending
    # any ore.
    # cost = solve('FUEL', 1, resources, reactions)
    # leftovers = defaultdict(int)

    # cost = 0
    # for i in range(10):
    #     resources = defaultdict(int)
    #     cost += solve('FUEL', 1, resources, reactions)

    #     for k,v in resources.items():
    #         leftovers[k] += resources[k]

    # print(f'leftovers {leftovers}')
    # c = solve('FUEL', 1, leftovers, reactions)
    # cost += c
    # print(f'1 cost {cost}, last was {c}')

    # resources = defaultdict(int)
    # cost = 0
    # for i in range(10):
    #     cost += solve('FUEL', 1, resources, reactions)
    # c = solve('FUEL', 1, resources, reactions)
    # cost += c
    # print(f'2 cost {cost} last was {c}')

    ore = 1000000000000
    fuel = 0
    resources = defaultdict(int)
    total_cost = 0
    cost_history = []
    cost_meta_history = []
    while ore > 0:
        cost = solve('FUEL', 1, resources, reactions)
        if cost == 2210736:
            print(f'Back to original cost after {fuel}')
        if cost > ore:
            break
        fuel += 1
        has_leftovers = [k for k in resources.keys() if resources[k] > 0]
        ore -= cost
        total_cost += cost
        if cost in cost_history:
            print(f'Already saw cost {cost} in {cost_history}')
            cost_meta_history.append(cost_history)
            cost_history = []
        cost_history.append(cost)
        if len(has_leftovers) == 0:
            print(f'no leftovers after {fuel} with cost {total_cost}')
            break

    # print(fuel)
runIt(part1, part2)