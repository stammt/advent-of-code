import aoc_utils
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
input = aoc_utils.PuzzleInput('input/input-day20.txt', testInput)

lines = input.getInputLines(test=False)

def areModulesInInitialState(modules):
    for m in modules:
        if modules[m]['type'] == '&':
            # Conjunction is in initial state if all memories are low (False)
            mem = modules[m]['memory']
            if len(list(filter(lambda x: mem[x] == True, mem))) > 0:
                return False
        elif modules[m]['type'] == '%':
            # FlipFlop is in initial state if it is off (False)
            if modules[m]['on']:
                return False
    return True


def part1(lines):
    # Module is a dict with keys type, [destinations]
    # Track modules by name
    modules = {}
    for line in lines:
        moduleStr, destinationsStr = line.split(' -> ')
        name = moduleStr if moduleStr == "broadcaster" else moduleStr[1:]
        type = moduleStr if moduleStr == "broadcaster" else moduleStr[:1]
        destinations = destinationsStr.split(", ")
        modules[name] = {'type': type, 'destinations': destinations}

    # Init conjunction modules to remember a low pulse from each input
    conjunctionModules = filter(lambda x: modules[x]['type'] == '&', modules)
    for module in conjunctionModules:
        inputs = filter(lambda x: module in modules[x]['destinations'], modules)
        mem = {}
        for i in inputs:
            mem[i] = False
        modules[module]['memory'] = mem

    # Init flip-flop modules to be off
    flipFlopModules = filter(lambda x: modules[x]['type'] == '%', modules)
    for module in flipFlopModules:
        modules[module]['on'] = False

    print(f'Sanity check: initial state is {areModulesInInitialState(modules)}')


    lowPulseCount = 0
    highPulseCount = 0
    buttonPushes = 0
    buttonPushesUntilInitialState = -1

    # keep going until we get back to the initial state
    while buttonPushes < 1000:
        if buttonPushes > 0 and areModulesInInitialState(modules):
            buttonPushesUntilInitialState = buttonPushes
            break

        buttonPushes += 1

        q = [{'high': False, 'source': 'button', 'destination': 'broadcaster'}]
        while len(q) > 0:
            pulse = q[0]
            del q[0]

            print(f'{pulse['source']} -{'high' if pulse['high'] else 'low'}-> {pulse['destination']}')

            if (pulse['high']):
                highPulseCount += 1
            else:
                lowPulseCount += 1

            if pulse['destination'] not in modules:
                continue

            module = modules[pulse['destination']]
            sendPulse = None
            if module['type'] == 'broadcaster':
                sendPulse = {'high': pulse['high']}
            elif module['type'] == '%':
                # flip-flop
                if not pulse['high']:
                    module['on'] = not module['on']
                    sendPulse = {'high': module['on']}
            elif module['type'] == '&':
                # conjunction
                mem = module['memory']
                mem[pulse['source']] = pulse['high']
                allHigh = len(list(filter(lambda x: mem[x] == False, mem))) == 0
                sendPulse = {'high': not allHigh}


            if sendPulse != None:
                for d in module['destinations']:
                    p = sendPulse.copy()
                    p['destination'] = d
                    p['source'] = pulse['destination']
                    q.append(p)

    if (buttonPushesUntilInitialState > 0):
        print(f'Reached initial state after {buttonPushesUntilInitialState}')
        print(f'{highPulseCount} high pulses * {lowPulseCount} low pulses = {lowPulseCount * highPulseCount}')
        m = 1000 / buttonPushesUntilInitialState
        print(f'Total: {(m * lowPulseCount) * (m * highPulseCount)} (m={m})')
    else:
        print(f'Never got back to initial state after {buttonPushes}')
        print(f'{highPulseCount} high pulses * {lowPulseCount} low pulses = {lowPulseCount * highPulseCount}')

def part2(lines):
    # Starting with the rx module, work backwards to find the sequence of
    # pulses that would have sent it a single low pulse.
    print('huh')

part2(lines)