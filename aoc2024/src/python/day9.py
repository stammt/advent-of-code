import time
from typing import Set, Tuple, List
from aoc_utils import  runIt, PuzzleInput, Point, Grid, add, sub
import functools
import math
import re
from itertools import combinations, permutations, product
import sys


testInput = r"""2333133121414131402"""

testInput2 = r"""12345"""

input = PuzzleInput('input/day9.txt', testInput)

lines = input.getInputLines(test=False)

def parse_disk(s) -> List[List[int]]:
    disk = [] # list of tuple (file id, file size, free space)
    i = 0
    id = 0
    while i < len(s):
        fileSize = s[i]
        i+=1
        freeSpace = 0 if i == len(s) else s[i]
        disk.append([id, int(fileSize), int(freeSpace)])
        i+=1
        id+=1
    return disk

def disk_to_str(disk) -> str:
    s = ''
    for b in disk:
        for i in range(b[1]):
            s += str(b[0])
        for i in range(b[2]):
            s += '.'
    return s

# index of the first block with free space
def first_free(disk) -> int:
    for i in range(len(disk)):
        if disk[i][2] > 0: return i
    return -1

def last_file(disk) -> int:
    for i in range(len(disk)-1, 0, -1):
        if disk[i][1] > 0: return i
    return -1

def part1():
    disk = parse_disk(lines[0])

    freeBlock = first_free(disk)
    lastBlock = last_file(disk)

    # print(disk)

    print(disk_to_str(disk))
    print(f'disk str len {len(disk_to_str(disk))}')
    # print(f'Moving from {lastBlock} to {freeBlock}')

    while lastBlock > freeBlock and lastBlock != -1 and freeBlock != -1:
        fileId = disk[lastBlock][0]
        fileSize = disk[lastBlock][1]

        freeSpace = disk[freeBlock][2]
        sizeDiff = min(fileSize, freeSpace)
        movedBlockFreeSpace = freeSpace - sizeDiff

        # print(f'Moving {fileSize} from {lastBlock} to {freeBlock}, can move {sizeDiff}')

        disk[freeBlock][2] = 0

        disk[lastBlock][1] = fileSize - sizeDiff
        disk[lastBlock][2] = disk[lastBlock][2] + sizeDiff

        movedFileBlock = [fileId, sizeDiff, movedBlockFreeSpace]
        disk.insert(freeBlock+1, movedFileBlock)


        freeBlock = first_free(disk)
        if sizeDiff < fileSize:
            lastBlock = last_file(disk)

        # print(disk)
        # print(disk_to_str(disk))

    # print(f'*** Done')
    # print(disk_to_str(disk))

    sum = 0
    pos = 0
    for block in disk:
        for i in range(block[1]):
            sum += (pos * block[0])
            pos += 1

    print(f'sum: {sum}')


def part2():
    print(f'asdf')

runIt(part1, part2)
