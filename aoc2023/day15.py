import aoc_utils
import math
import re
import itertools

testInput = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
input = aoc_utils.PuzzleInput('input-day15.txt', testInput)

lines = input.getInputLines(test=False)

def myHash(s):
    v = 0
    for c in s:
        code = ord(c)
        v += code
        v *= 17
        v %= 256
    return v

def part1(lines):
    steps = lines[0].split(',')
    sum = 0

    for s in steps:
        h = myHash(s)
        print(f'hash {h} from {s}')
        sum += h

    print(f'Sum: {sum}')
        
# Finds the index of the label,focalLength for this label in the box.
# Just do a simple linear search of the box.
def findIndexOfLabel(box, label):
    for i, j in enumerate(box):
        if j[0] == label:
            return i
    return None

def part2(lines):
    steps = lines[0].split(',')

    # Each box is an array of pairs (label, focalLength)
    boxes = [[] for i in range(256)]

    for s in steps:
        if s.find('=') != -1:
            label, focalLength = s.split('=')
            box = myHash(label)
            i = findIndexOfLabel(boxes[box], label)

            if i != None:
                # Replace the old with the new
                boxes[box][i] = (label, int(focalLength))
            else:
                # Append the new lens
                boxes[box].append((label, int(focalLength)))
        else:
            label = s[:-1]
            box = myHash(label)
            i = findIndexOfLabel(boxes[box], label)
            if i != None:
                del boxes[box][i]

    sum = 0
    for i in range(len(boxes)):
        for j in range(len(boxes[i])):
            fp = (i+1) * (j+1) * boxes[i][j][1]
            print(f'fp: {fp}')
            sum += fp

    # printBoxes(boxes, labelToIndex)
    print(f'Focusing power sum: {sum}')



part2(lines)