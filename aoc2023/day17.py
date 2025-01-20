
from collections import defaultdict
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
input = PuzzleInput('input-day17.txt', testInput)

lines = input.getInputLines(test=True)


def lava_dijkstra(start, goal, grid: Grid) -> int:
    # treat each node as a tuple of (p, facing), neighbors are 1,2,3 to right and left
    prev = dict()

    q = {(p, dir) for p in grid.keys() for dir in cardinal_directions}
    dist = {p: sys.maxsize for p in q}
    dist[(start, East)] = 0
    dist[(start, South)] = 0

    while len(q) > 0:
        u = min([n for n in q], key=lambda x: dist[x])
        q.remove(u)

        if u[0] == goal:
            return dist[u]

        p = u[0]
        facing = u[1]

        # neighbors are 1, 2, 3 steps to the right or left
        rfacing = make_turn(facing, 'R')
        rloss = 0
        pr = p
        for i in range(1, 4):
            pr = add(pr, rfacing)
            if pr in grid:
                v = (pr, rfacing)
                rloss += int(grid[pr])

                alt = dist[u] + rloss
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        # rneighbors = [(pr, rfacing) for pr in [add(p, mul(rfacing, i)) for i in range(1, 4)] if pr in grid]
        lfacing = make_turn(facing, 'L')
        # lneighbors = [(pl, lfacing) for pl in [add(p, mul(lfacing, i)) for i in range(1, 4)] if pl in grid]
        lloss = 0
        pl = p
        for i in range(1, 4):
            pl = add(pl, lfacing)
            if (pl in grid):
                v = (pl, lfacing)
                lloss += int(grid[pl])

                alt = dist[u] + lloss
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

    return -1


def part1():
    grid = Grid(lines)
    goal = (grid.size[0] - 1, grid.size[1] - 1)
    heatLoss = lava_dijkstra((0, 0), goal, grid)
    print(f'Heat loss: {heatLoss} ')
    # got answer 956 in 231 seconds...
    # (test took 17ms)

def part2():
    print('nyi')

runIt(part1, part2)