from aoc_utils import PuzzleInput, runIt
import functools
import math
import re
from itertools import groupby
import sys

testInput = r"""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
input = PuzzleInput('input-day19.txt', testInput)

lines = input.getInputLines(test=False)

def part1():
    sections = [list(p) for _,p in groupby(lines, key=lambda x: x != '') if p]
    workflows = dict()
    for line in sections[0]:
        name = line[0:line.find('{')]
        ruleString = line[len(name)+1:-1]
        rules = [] # list of tuples: (attr, </>, value, destination) or just destination for the fallback
        for r in ruleString.split(','):
            colon = r.find(':')
            if colon == -1:
                rules.append(tuple([r]))
            else:
                rules.append((r[0], r[1], int(r[2:colon]), r[colon+1:]))
        workflows[name] = rules

    parts = []
    for line in sections[2]:
        values = line[1:-1].split(',')
        d = dict()
        for v in values:
            [k,n] = v.split('=')
            d[k] = int(n)
        parts.append(d)
    
    # print(workflows)
    # print(parts)

    accepted = []
    rejected = []
    for part in parts:
        # print(f'\nPart: {part}')
        ruleName = 'in'
        while ruleName != 'A' and ruleName != 'R':
            flow = workflows[ruleName]
            # print(f'Evaluating workflow {ruleName} : {flow}')
            for rule in flow:
                # print(f'rule: {rule}')
                if len(rule) == 1:
                    # print(f' falling back to {rule[0]}')
                    ruleName = rule[0]
                    break
                v1 = part[rule[0]]
                v2 = rule[2]
                # print(f'v1={v1}, v2={v2}, op={rule[1]}')
                if (rule[1] == '>' and v1 > v2) or (rule[1] == '<' and v1 < v2):
                    # print(f' passed rule {rule}, next is {rule[3]}')
                    ruleName = rule[3]
                    break
        if ruleName == 'A':
            accepted.append(part)
        elif ruleName == 'R':
            rejected.append(part)
        else:
            print(f'Not sure what to do with rule {ruleName} for {part}')

    print(f'{len(accepted)} accepted, {len(rejected)} rejected')

    total = sum([p['x'] + p['m'] + p['a'] + p['s'] for p in accepted])
    print(f'Total: {total}')

def part2():
    print('nyi')

runIt(part1, part2)