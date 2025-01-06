from collections import defaultdict
import time
from typing import Set, Tuple, List
from aoc_utils import  mul, runIt, PuzzleInput, split_on_empty_lines, sub, Grid, Point, cardinal_directions, add, North, South, East, West
import functools
import math
import re
from itertools import chain, combinations, permutations, product
import sys
import numpy


testInput = r"""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

testInput2 = r"""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

WALL = '#'

input = PuzzleInput('input/day16.txt', testInput2)
lines = input.getInputLines(test=False)
grid = Grid(lines)
start = grid.find('S')
finish = grid.find('E')


# return a tuple of distances, paths
def dijkstra() -> Tuple[dict, dict]:
    print(f'from {start} to {finish}')
    q = {(p, d) for d in cardinal_directions for p in grid.keys() if grid[p] != WALL}
    dist = {(start, East): 0}
    prev = {}

    # def min_dist(k): dist[k] if k in dist else sys.maxsize
    while len(q) > 0:
        u = min(q, key=lambda x: dist[x] if x in dist else sys.maxsize)
        min_dist = dist[u] if u in dist else sys.maxsize
        # print(f'looking at {u} with dist {min_dist}')
        q.remove(u)

        def score(a, b): return 1001 if a[1] != b[1] else 1

        neighbors = [(add(u[0], d), d) for d in cardinal_directions if (add(u[0], d), d) in q]
        # print(f'Found neighbors: {neighbors}')
        for n in neighbors:
            # print(f'Score from {u} to {n} is {score(u, n)}')
            alt = min_dist + score(u, n)
            if n not in dist or alt < dist[n]:
                dist[n] = alt
                prev[n] = [u]
            elif alt == dist[n]:
                prev[n].append(u)

    return (dist, prev)

def all_seats(p, prev) -> Set[Point]:
    seats = set()
    seats.add(p[0])
    if p in prev:
        for s in prev[p]:
            seats = seats | all_seats(s, prev)
    return seats

def part1():
    distances = dijkstra()
    # print(distances)
    shortest = min(v for k,v in distances[0].items() if k[0] == finish)
    finish_with_dir = list(k for k,v in distances[0].items() if k[0] == finish and v == shortest) 
    path_count = len(finish_with_dir)
    print(f'shortest: {shortest} out of {path_count}')

    ### Part 2:
    seats = set()
    # print(f'prev: {distances[1]}')
    for f in finish_with_dir:
        seats = seats | all_seats(f, distances[1])

    print(f'seats: {len(seats)}')


def part2():
    print(f'nyi')

runIt(part1, part2)
