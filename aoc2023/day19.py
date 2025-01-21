from operator import mul
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

def parse_workflows(workflow_section) -> dict:
    workflows = dict()
    for line in workflow_section:
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
    return workflows

def parse_parts(parts_section) -> list:
    parts = []
    for line in parts_section:
        values = line[1:-1].split(',')
        d = dict()
        for v in values:
            [k,n] = v.split('=')
            d[k] = int(n)
        parts.append(d)
    return parts

def part1():
    sections = [list(p) for _,p in groupby(lines, key=lambda x: x != '') if p]
    workflows = parse_workflows(sections[0])
    parts = parse_parts(sections[2])

    accepted = []
    rejected = []
    for part in parts:
        ruleName = 'in'
        while ruleName != 'A' and ruleName != 'R':
            flow = workflows[ruleName]
            for rule in flow:
                if len(rule) == 1:
                    ruleName = rule[0]
                    break
                v1 = part[rule[0]]
                v2 = rule[2]
                if (rule[1] == '>' and v1 > v2) or (rule[1] == '<' and v1 < v2):
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

def solve(workflow_name: str, ranges: dict[str, range], workflows) -> int:
    # for each rule, recurse, with the ranges restricted for that rule
    # if we hit 'A', return the final range
    # if multiple paths return from 'A', merge the ranges - how to deal with gaps?
    if workflow_name == 'A':
        print(f'Reached A  with {ranges}')
        return math.prod(len(c) for c in [ranges[k] for k in ['x', 'm', 'a', 's']])
    elif workflow_name == 'R':
        return 0

    count = 0

    workflow = workflows[workflow_name]
    # print(f'Evaluating workflow {workflow_name} : {workflow} : {ranges}')
    updated = dict(ranges)
    for rule in workflow:            
        if len(rule) == 1:
            # fallback rule
            count += solve(rule[0], updated, workflows)
        else:
            a = rule[0]
            r = ranges[a]
            op = rule[1]
            b = rule[2]

            r_inverse = r
            if op == '>':
                # remove a <= b from the range
                r_inverse = range(r.start, b+1)
                r = range(b + 1, r.stop)
            elif op == '<':
                # remove a >= b from the range
                r_inverse = range(b, r.stop)
                r = range(r.start, b)

            # updated = dict(ranges)

            flow_rules = dict(updated)
            flow_rules[a] = r
            count += solve(rule[3], flow_rules, workflows)

            updated[a] = r_inverse # needs to be inverse of this rule

    return count


def part2():
    sections = [list(p) for _,p in groupby(lines, key=lambda x: x != '') if p]
    workflows = parse_workflows(sections[0])

    # Start with 'in', range(1,4001) for each letter, find all paths to 'A' and find the union of their rules?
    ranges = {k: range(1, 4001) for k in ['x', 'm', 'a', 's']}
    # start = workflows['in']
    count = solve('in', ranges, workflows)

    # 196723013358875 too high
    print(f'Count {count}')

runIt(part1, part2)