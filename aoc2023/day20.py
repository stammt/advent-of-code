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
        destinations = tuple(destinationsStr.split(", "))
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
    for pushes in range(10000):
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
    # From the input:
    # &rs -> rx
    # So we need all inputs to rs to be High so it will send a Low pulse to rx
    # bt, dl, fw, rv need to send High

    # Find when all of them have sent a High pulse without sending a Low pulse afterwards

    broadcaster = []
    # dict of module name -> tuple of type, state, destinations
    modules: dict[str:tuple(str, dict[str, bool], list[str])] = {}
    conjnction_inputs = defaultdict(list)
    for line in lines:
        moduleStr, destinationsStr = line.split(' -> ')
        name = moduleStr if moduleStr == "broadcaster" else moduleStr[1:]
        type = moduleStr if moduleStr == "broadcaster" else moduleStr[:1]
        destinations = tuple(destinationsStr.split(", "))
        if name == "broadcaster":
            broadcaster = destinations
            modules[name] = Module('broadcaster', defaultdict(bool), destinations)
        else:
            modules[name] = Module(type, defaultdict(bool), destinations)
        for d in destinations:
            conjnction_inputs[d].append(name)

    # Initialize the inputs of the conjunctions to False
    for name in conjnction_inputs.keys():
        if name in modules and modules[name][0] == CONJUNCTION:
            for i in conjnction_inputs[name]:
                modules[name][1][i] = False


    # # walk back from rx to broadcaster
    # dest = deque( [('rx', 0)])
    # seen = set()
    # while dest:
    #     d, level = dest.popleft()
    #     for k,v in modules.items():
    #         if d in v.outputs:
    #             if (k,d) not in seen:
    #                 print(f'{'..'* level} {v.type}{k} goes to {d}')
    #                 dest.append((k, level + 1))
    #                 seen.add((k,d))



    # Queue of pulses as a tuple (high/low, sender, receiver)
    q = deque()
    pushes = 0
    while pushes < 100000:
        pushes += 1
        q.extend([(False, 'broadcaster', m) for m in broadcaster])

        # print(f'bt: {modules['bt']}')
        # print(f'dl: {modules['dl']}')
        # print(f'fr: {modules['fr']}')
        # print(f'rv: {modules['rv']}')
        if any(modules['rs'].state.values()):
            print(f'{pushes} rs: {modules['rs']}')

        print(f'{pushes} {[modules[x].state[STATE] for x in broadcaster]}')


        while q:
            pulse = q.popleft()
            # print(f'{pulse[1]} -{'high' if pulse[0] else 'low'}-> {pulse[2]}')

            if pulse[2] == 'rx':

                # print(f'rx: {pulse[0]} after {pushes}')
                if pulse[0] == False:
                    print(f'rx got a low pulse: {pushes}')
                    return
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
                # if pulse[2] == 'mj':
                #     print(f'At push {pushes} {pulse[2]} is {receiver}')
                sendPulse = len(receiver.state) == 0 or not all(receiver.state.values())
                # if pulse[2] == 'rs':
                #     print(f'At push {pushes} {pulse[2]} is {receiver} will send {sendPulse}')

            if sendPulse != None:
                for d in receiver.outputs:
                    q.append((sendPulse, pulse[2], d))

    print(f'Never got a low pulse to rx...')

runIt(part1, part2)