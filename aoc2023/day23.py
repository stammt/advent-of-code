from aoc_utils import PuzzleInput, runIt, Point, cardinal_directions, add, Grid, North, South, East, West, reconstruct_path, manhattan_distance
import functools
import math
import re
import itertools
import sys
from collections import Counter, defaultdict, deque

testInput = r"""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
input = PuzzleInput('input-day23.txt', testInput)

lines = input.getInputLines(test=False)

def neighbor_dirs(c):
    if c == '.': return cardinal_directions
    elif c == '^': return {North}
    elif c == 'v': return {South}
    elif c == '>': return {East}
    else: return {West}



def longest_path(start, finish, grid, visited=set()):
    if start == finish:
        return 0
    
    result = -sys.maxsize

    # Add the current node to visited for the duration of this recursion, but
    # let other paths see it later.
    visited.add(start)
    for n in grid.neighbors(start, neighbor_dirs(grid[start])):
        if grid[n] != '#' and n not in visited :
            result = max(result, longest_path(n, finish, grid, visited) + 1)
    visited.remove(start)

    return result

def follow(p: Point, n: Point, cost: int, grid):
    # follow a path with no branches, eventually returning a tuple of (last point, step count)
    neighbors = [d for d in grid.neighbors(n) if grid[d] != '#' and d != p]
    if len(neighbors) == 1:
        return follow(n, neighbors[0], cost + 1, grid)
    else:
        return (n, cost)

def grid_to_graph(grid: Grid):
    # reduce the maze grid to a graph where the vertices are points where the
    # path can diverge, and the cost of each node is the number of nodes between
    # it and the previous vertex.
    graph = defaultdict(set) # Node -> neighbors
    costs = defaultdict(int) # Node -> cost

    for p in grid:
        if grid[p] == '#': continue # ignore walls
        neighbors = [d for d in grid.neighbors(p) if grid[d] != '#']
        if len(neighbors) == 2: continue # only use points where the path can branch
        for n in neighbors:
            (last, cost) = follow(p, n, 1, grid)
            graph[p].add(last)
            costs[(p, last)] = cost

    return graph,costs

def longest_path_graph(start, finish, graph, costs, visited = set()) -> int:
    edges = graph[start]
    if finish in edges:
        return costs[(start, finish)]
    
    result = 0
    for e in edges:
        if e not in visited:
            # Add the current node to visited for the duration of this recursion, but
            # let other paths see it later.
            visited.add(start)
            result = max(result, longest_path_graph(e, finish, graph, costs, visited) + costs[(start, e)])
            visited.remove(start)

    return result


def part1():
    sys.setrecursionlimit(10_000)
    start = (lines[0].index('.'), 0)
    finish = (lines[len(lines) - 1].index('.'), len(lines) - 1)
    grid = Grid(lines)

    result = longest_path(start, finish, grid)

    # 1998
    print(f'Logest: {result}')
    
def part2():
    start = (lines[0].index('.'), 0)
    finish = (lines[len(lines) - 1].index('.'), len(lines) - 1)
    grid = Grid(lines)

    graph, costs = grid_to_graph(grid)

    result = longest_path_graph(start, finish, graph, costs)

    # 6434
    print(f'Logest: {result}')

runIt(part1, part2)