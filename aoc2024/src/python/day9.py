from collections import defaultdict
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

def parse_disk(s) -> List[int]:
    disk = [] 
    i = 0
    id = 0
    while i < len(s):
        fileSize = int(s[i])
        i+=1
        freeSpace = 0 if i == len(s) else int(s[i])
        disk.extend([id for x in range(fileSize)])
        disk.extend([-1 for x in range(freeSpace)])
        i+=1
        id+=1
    return disk


def last_file(disk, before=-1) -> int:
    if before == -1:
        before = len(disk) - 1
    for i in range(before, 0, -1):
        if disk[i] >= 0: return i
    return -1

def part1():
    disk = parse_disk(lines[0])

    freeBlock = disk.index(-1)
    lastBlock = last_file(disk)

    while lastBlock > freeBlock and lastBlock != -1 and freeBlock != -1:
        disk[freeBlock] = disk[lastBlock]
        disk[lastBlock] = -1

        # more pythonic but 10x slower!
        # freeBlock = next(iter((i for i in range(freeBlock + 1, lastBlock)    if disk[i] == -1)))
        # lastBlock  = next(iter((i for i in range(lastBlock - 1, 0, -1) if disk[i] != -1)))

        while (disk[freeBlock] >= 0):
            freeBlock += 1
        while (disk[lastBlock] < 0):
            lastBlock -= 1

    sum = 0
    for i in range(len(disk)):
        if (disk[i] != -1):
            sum += (i * disk[i])

    print(f'sum: {sum}')


def file_slices(diskStr) -> List[slice]:
    slices = []
    block = 0
    for i, length in enumerate(diskStr):
        if i%2 == 0:
            slices.append(slice(block, block + int(length)))
        block += int(length)
    slices.reverse()
    return slices

def part2():
    disk = parse_disk(lines[0])
    # fileIds = sorted(list(set(disk)))
    # fileIds.remove(-1)
    # fileIds.reverse()
    # print(file_slices(lines[0]))
    freeStarts = defaultdict(int)

    for block in file_slices(lines[0]):
        fileStart = block.start
        fileEnd = block.stop
        # while fileEnd < len(disk) and disk[fileEnd] == disk[fileStart]:
        #     fileEnd += 1
        fileLen = fileEnd - fileStart
        freeStart = -1

        freeRun = 0
        for i in range(disk.index(-1, freeStarts[fileLen]), len(disk)):
            freeStarts[fileLen] = i
            if i >= fileStart:
                break;
            elif disk[i] == -1:
                freeRun += 1
                if freeRun == fileLen:
                    freeStart = i + 1 - fileLen
                    break
            else:
                freeRun = 0

        # freeRange = [-1 for i in range(fileLen)]
        # for fs in (i for i,e in enumerate(disk[:fileStart]) if e == -1):
        #     if disk[fs:fs+fileLen] == freeRange:
        #         freeStart = fs
        #         break
        if freeStart != -1 and freeStart < fileStart:
            for i in range(freeStart, freeStart+fileLen):
                disk[i] = disk[fileStart]
            for i in range(fileStart, fileEnd):
                disk[i] = -1

    sum = 0
    for i in range(len(disk)):
        if (disk[i] != -1):
            sum += (i * disk[i])

    print(f'sum: {sum}')

runIt(part1, part2)
