
from collections import defaultdict
import math
import re
import itertools
import sys

from aoc_utils import Direction, reconstruct_path, runIt, PuzzleInput, Grid, Point, add, sub, cardinal_directions, manhattan_distance

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

# do a dfs, pass last two nodes through to check neighbors, memoize the best so far so we can cut off branches
def dfs(start: Point, goal: Point, grid: Grid) -> int:
    q = [(start, None, None, None, 0)]
    bestLosses = dict()

    result = sys.maxsize
    # resultPath = []
    while len(q) > 0:
        current = q.pop()

        k = (current[0], current[1], current[2], current[3])
        if k in bestLosses and bestLosses[k] < current[4]:
            # print(f'Skipping {k}')
            continue
        
        bestLosses[k] = current[4]

        lastDir = current[1]
        lastDir2 = current[2]
        lastDir3 = current[3]
        loss = current[4]
        dirs = set(cardinal_directions)
        if lastDir != None:
            # print(f'lastDir {lastDir} removing {sub((0, 0), lastDir)}')
            dirs.remove(sub((0, 0), lastDir)) # don't go backwards
            if (lastDir == lastDir2 and lastDir == lastDir3): # don't keep going more than 3 segments
                dirs.remove(lastDir)

        neighbors = grid.neighbors(current[0], dirs)
        neighbors = sorted(neighbors, key=lambda x: manhattan_distance(x, goal), reverse=True)
        # print(f'Checking neighbors of {current[0]}: {neighbors}')
        # result = sys.maxsize
        for n in neighbors:
            if n == goal:
                print(f'Reached goal with {loss + int(grid[n])}')
                if result > loss + int(grid[n]):
                    result = loss + int(grid[n])
                    # resultPath.append(n)
                # result = min(result, loss + int(grid[n]))
            else:
                d = sub(n, current[0])
                # p = list(current[5])
                # p.append(n)
                nk = (n, d, lastDir, lastDir2)
                if nk not in bestLosses or bestLosses[nk] > loss + int(grid[n]):
                    bestLosses[nk] = loss + int(grid[n])

                q.append((n, d, lastDir, lastDir2, loss + int(grid[n])))
        
    # print(f'Final result {result} with {resultPath}')
    # overlay = dict()
    # for p in resultPath:
    #     overlay[p] = '*'
    # print(grid.to_string(overlay))
    return result


def part1():
    grid = Grid(lines)
    goal = (grid.size[0] - 1, grid.size[1] - 1)
    print(f'Goal: {goal} ')
    # path = lavA_star((0, 0), goal, lambda p: manhattan_distance(p, goal), grid)
    # path = lava_dijkstra((0, 0), goal, grid)
    heatLoss = dfs((0, 0), goal, grid)
    print(f'Heat loss: {heatLoss} ')

    ## 1526 too high
    # overlay = {p: '*' for p in path}
    # print(grid.to_string(overlay))

def part2():
    print('nyi')

runIt(part1, part2)