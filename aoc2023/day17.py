
from collections import defaultdict
from heapq import heappop, heappush
import math
import re
import itertools
import sys

from aoc_utils import Direction, make_turn, reconstruct_path, runIt, PuzzleInput, Grid, Point, add, sub, mul, cardinal_directions, manhattan_distance, North, South, East, West

testInput = r"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

testInput2 = r"""111111111111
999999999991
999999999991
999999999991
999999999991"""

input = PuzzleInput('input-day17.txt', testInput)

lines = input.getInputLines(test=False)



def lavA_star(start, goal, h, min_steps, max_steps, grid: Grid) -> int: # list[Point]:
    openSet = []
    hStart = h(start)
    heappush(openSet, (hStart, (start, South)))
    heappush(openSet, (hStart, (start, East)))

    cameFrom: dict[tuple[Point, Point], tuple[Point, Point]] = dict()

    # For node n, gScore[n] is the currently known cost of the cheapest path from start to n.
    gScore: dict[tuple[Point, Point], int]  = defaultdict(lambda: sys.maxsize)
    gScore[(start, South)] = 0
    gScore[(start, East)] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore: dict[tuple[Point, Point], int] = defaultdict(lambda: sys.maxsize)
    fScore[(start, South)] = hStart
    fScore[(start, East)] = hStart

    # Turn L/R from current facing, and take as many steps as possible treating each as a "neighbor"
    def turn_and_step(dir, current):
        facing = make_turn(current[1], dir)
        loss = 0
        p = current[0]
        for i in range(1, max_steps+1):
            p = add(p, facing)
            if p not in grid:
                break

            v = (p, facing)
            loss += int(grid[p])

            if (i >= min_steps):
                tentative_gScore = gScore[current] + loss
                if tentative_gScore < gScore[v]:
                    cameFrom[v] = current
                    gScore[v] = tentative_gScore
                    fScore[v] = tentative_gScore + h(v[0])
                    if v not in openSet:
                        heappush(openSet, (fScore[v], v))

    while len(openSet) > 0:
        current = heappop(openSet)[1]
        if (current[0] == goal):
            # print_path(current, cameFrom, grid)
            return gScore[current] # reconstruct_path(goal, cameFrom)
        
        # openSet.remove(current)

        turn_and_step('L', current)
        turn_and_step('R', current)

    return -1

def print_path(goal, cameFrom, grid):
    overlay = dict()
    p = goal
    while p in cameFrom:
        overlay[p[0]] = '*'
        p = cameFrom[p]
    print(grid.to_string(overlay))

def part1():
    grid = Grid(lines)
    goal = (grid.size[0] - 1, grid.size[1] - 1)
    heatLoss = lavA_star((0, 0), goal, lambda x: manhattan_distance(x, goal), 1, 3, grid)
    print(f'Heat loss: {heatLoss} ')
    # got answer 956 in 231 seconds with dijkstra, 10 seconds with modified A*, 2.5seconds using pririty queue in A*
    # (test took 17ms, 6ms with A*)

def part2():
    grid = Grid(lines)
    goal = (grid.size[0] - 1, grid.size[1] - 1)
    heatLoss = lavA_star((0, 0), goal, lambda x: manhattan_distance(x, goal), 4, 10, grid)
    print(f'Heat loss: {heatLoss} ')
    # got answer 1106 in 31 seconds with modified A*, 10 seconds using priority queue in A*

runIt(part1, part2)