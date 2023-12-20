import aoc_utils
import functools
import math
import re
import itertools
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
input = aoc_utils.PuzzleInput('input-day19.txt', testInput)

lines = input.getInputLines(test=True)

def mergeRanges(r1, r2):
    result = {}
    for a in r1:
        range1 = r1[a]
        if a not in r2:
            result[a] = range1
        else:
            range2 = r2[a]
            merged = (max(range1[0], range2[0]), min(range1[1], range2[1]))
            result[a] = merged
    # Then add the rest of the values from r2
    for a in filter(lambda x: x not in result, r2):
        result[a] = r2[a]
    return result

class WorkflowRule:
    attr = None
    gt = True
    value = None

    def __init__(self, attr, gt, value):
        self.attr = attr
        self.gt = gt
        self.value = value

    # Return True if the item passes the test
    def eval(self, item):
        itemValue = item[self.attr]
        return (itemValue > self.value) if self.gt else (itemValue < self.value)
    
    # return a map of (min, max) tuple keyed by the attr name
    def getAttrRanges(self):
        maxValue = 4000
        if self.gt:
            return {self.attr: (self.value + 1, maxValue)}
        else:
            return {self.attr: (1, self.value - 1)}
    
    def __str__(self):
        return f'<Rule: {self.attr} {'>' if self.gt else '<'} {self.value}>'
    
class FallbackRule:
    rules = None

    def __init__(self, rules):
        self.rules = list(rules) # make our own shallow copy

    def eval(self, item):
        # If the item passes any rule, it fails the fallback
        for rule in self.rules:
            if rule.eval(item):
                return False
        return True
    
    # return a map of (min, max) tuple keyed by the attr name
    def getAttrRanges(self):
        maxValue = 4000
        ranges = {}
        for rule in self.rules:
            # invert the rule, since this is the fallback
            ruleRange = {}
            if rule.gt:
                # lte the value
                ruleRange[rule.attr] = (1, rule.value)
            else:
                # gte the value
                ruleRange[rule.attr] = (rule.value, maxValue)
            ranges = mergeRanges(ruleRange, ranges)
        return ranges
            
    
    def __str__(self):
        s = '<FallbackRule'
        for r in self.rules:
            s += ' ' + str(r)
        return s + '>'
    
class Workflow:
    # list of (rule,workflow name) pairs
    rules = []
    fallback = None

    def __init__(self, rules, fallback):
        self.rules = rules
        self.fallback = fallback

    # Returns A for accept, R for reject, or the name of the next workflow
    def eval(self, item):
        for rule in self.rules:
            if rule[0].eval(item):
                return rule[1]
        return self.fallback

# Returns (name, workflow) tuple
def parseWorkflow(line):
    openBrace = line.find('{')
    name = line[:openBrace]
    ruleStrings = line[openBrace+1:-1].split(',')
    rules = []
    fallback = None
    for rs in ruleStrings:
        if ':' in rs:
            expr, result = rs.split(':')
            if '>' in expr:
                attr, value = expr.split('>')
                rules.append((WorkflowRule(attr, True, int(value)), result))
            else:
                attr, value = expr.split('<')
                rules.append((WorkflowRule(attr, False, int(value)), result))
        else:
            fallback = rs

    return (name, Workflow(rules, fallback))

def parseItem(line):
    attrs = line[1:-1].split(',')
    item = {}
    for a in attrs:
        k, v = a.split('=')
        item[k] = int(v)
    return item



def part1(lines):
    workflows = {}
    items = []
    parsingWorkflows = True
    for line in lines:
        if len(line.strip()) == 0:
            parsingWorkflows = False
        elif parsingWorkflows:
            name, workflow = parseWorkflow(line)
            workflows[name] = workflow
        else:
            items.append(parseItem(line))

    accepted = []
    for item in items:
        workflow = workflows['in']
        while workflow != None:
            result = workflow.eval(item)
            if result == 'A':
                print(f'Accepted {item}')
                accepted.append(item)
                workflow = None
            elif result == 'R':
                workflow = None
            else:
                workflow = workflows[result]

    print(f'Accepted {len(accepted)} items')

    sum = 0
    for item in accepted:
        sum += item['x'] + item['m'] + item['a'] + item['s']

    print(f'xmas sum: {sum}')

# path is a list of rules to be met to get to this node
# returns a list of list of rules to get to each accepted state
def dfsToAccepted(root, path, workflows):
    allResults = []

    # dfs through each rule
    fallbackRules = []
    for rule in root.rules:

        if rule[1] == 'A':
            allResults.append(path + [rule[0]])
        elif rule[1] != 'R':
            node = workflows[rule[1]]
            fallbackList = [] if len(fallbackRules) == 0 else [FallbackRule(fallbackRules)]
            result = dfsToAccepted(node, path + fallbackList + [rule[0]], workflows)
            for r in result:
                allResults.append(r)
        fallbackRules.append(rule[0])

    # the fallback workflow is a rule that contains the inverse
    # of the other rules
    # fallbackRules = list(map(lambda x: x[0], root.rules))
    if root.fallback == 'A':
        allResults.append(path + [FallbackRule(fallbackRules)])
    elif root.fallback != 'R':
        fallbackWorkflow = workflows[root.fallback]
        result = dfsToAccepted(fallbackWorkflow, path + [FallbackRule(fallbackRules)], workflows)
        for r in result:
            allResults.append(r)

    return allResults

def printPaths(workflowList):
    result = ''
    for w in workflowList:
        result += str(w)
    return result

def part2(lines):
    workflows = {}
    items = []
    parsingWorkflows = True
    for line in lines:
        if len(line.strip()) == 0:
            parsingWorkflows = False
        elif parsingWorkflows:
            name, workflow = parseWorkflow(line)
            workflows[name] = workflow
        else:
            items.append(parseItem(line))

    # Start with the "in" workflow and do a DFS through
    # each rule, tracking the path to any 'A' state
    root = workflows['in']
    paths = dfsToAccepted(root, [], workflows)
    print(f'Found {len(paths)} paths')
    for p in paths:
        print('\n')
        for r in p:
            print(r)

    # Then for each path, find the range for each xmas attribute and multiply them together
    maxValue = 4000
    prods = []
    for p in paths:
        print(f'\nPath: {printPaths(p)}')
        ranges = {'x': (1, maxValue), 'm': (1, maxValue), 'a': (1, maxValue), 's': (1, maxValue)}
        for rule in p:
            ruleRange = rule.getAttrRanges()
            print(f'Range for rule <{rule}>: {ruleRange}')
            ranges = mergeRanges(ranges, ruleRange)
            print(f'Merged in, ranges now: {ranges}')

        combos = []
        for c in 'xmas':
            combos.append(ranges[c][1] - ranges[c][0] + 1)
        comboCount = functools.reduce(lambda x, y: x * y, combos)
        print(f'Final ranges: {ranges}')
        print(f'Multipled {combos} to get {comboCount}')
        prods.append(comboCount)

    print(f'sum of {prods} = {sum(prods)}')

    #167409079868000
    #207345096440000





part2(lines)