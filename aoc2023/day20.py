from collections import defaultdict, deque, namedtuple
from aoc_utils import runIt, PuzzleInput
import functools
import math
import re
import itertools
import sys

testInputSimple = r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
testInput = r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
input = PuzzleInput('input-day20.txt', testInput)

lines = input.getInputLines(test=False)

FLIPFLOP = '%'
STATE = 'state'
CONJUNCTION = '&'
Module = namedtuple('Module', ['type', 'state', 'outputs'])

def part1():

    broadcaster = []
    # dict of module name -> tuple of type, state, destinations
    modules: dict[str:tuple(str, dict[str, bool], list[str])] = {}
    conjnction_inputs = defaultdict(list)
    for line in lines:
        moduleStr, destinationsStr = line.split(' -> ')
        name = moduleStr if moduleStr == "broadcaster" else moduleStr[1:]
        type = moduleStr if moduleStr == "broadcaster" else moduleStr[:1]
        destinations = destinationsStr.split(", ")
        if name == "broadcaster":
            broadcaster = destinations
        else:
            modules[name] = Module(type, defaultdict(bool), destinations)
        for d in destinations:
            conjnction_inputs[d].append(name)

    # Initialize the inputs of the conjunctions to False
    for name in conjnction_inputs.keys():
        if name in modules and modules[name][0] == CONJUNCTION:
            for i in conjnction_inputs[name]:
                modules[name][1][i] = False

    lowPulseCount = 0
    highPulseCount = 0
    # Queue of pulses as a tuple (high/low, sender, receiver)
    q = deque()
    for pushes in range(1000):
        lowPulseCount += 1 # button sends a low pulse
        q.extend([(False, 'broadcaster', m) for m in broadcaster])

        while q:
            pulse = q.popleft()
            # print(f'{pulse[1]} -{'high' if pulse[0] else 'low'}-> {pulse[2]}')

            if (pulse[0]):
                highPulseCount += 1
            else:
                lowPulseCount += 1

            if pulse[2] not in modules:
                continue

            receiver = modules[pulse[2]]
            sendPulse = None

            if receiver.type == FLIPFLOP:
                # flip-flop
                if pulse[0] == False:
                    receiver.state[STATE] = not receiver.state[STATE]
                    sendPulse = receiver[1][STATE]
            else:
                # conjunction
                receiver.state[pulse[1]] = pulse[0]
                # If any inputs are low, send a high pulse
                sendPulse = len(receiver.state) == 0 or not all(receiver.state.values())


            if sendPulse != None:
                for d in receiver.outputs:
                    q.append((sendPulse, pulse[2], d))

    print(f'{highPulseCount} high pulses * {lowPulseCount} low pulses = {lowPulseCount * highPulseCount}')

def part2():
    # Starting with the rx module, work backwards to find the sequence of
    # pulses that would have sent it a single low pulse.
    print('huh')

runIt(part1, part2)