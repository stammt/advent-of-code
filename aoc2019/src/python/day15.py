from collections import defaultdict
import os
import time
from aoc_utils import A_star, Grid, PuzzleInput, manhattan_distance, runIt, splitInts, North, South, East, West, turn, add, cardinal_directions
from itertools import count
from intcode import STATE_HALTED, Intcode

testInput = r""""""
input = PuzzleInput('input/day15.txt', testInput)

lines = input.getInputLines(test=False)

WALL = '#'
EMPTY = '.'
GOAL = 'O'

def explore_dir(npos, input, pop_input, path, grid, computer):
    if npos not in grid:
        computer.run_with_input([input])
        status_north = computer.output[0]
        if status_north == 2:
            grid[npos] = GOAL
            print(f'Found goal at {npos}')
        grid[npos] = WALL if status_north == 0 else EMPTY if status_north == 1 else GOAL
        if status_north != 0:
            explore(npos, path + [input], grid, computer)
            computer.run_with_input([pop_input])

def explore(pos, path, grid, computer):
    npos = add(pos, North)
    explore_dir(npos, 1, 2, path, grid, computer)

    spos = add(pos, South)
    explore_dir(spos, 2, 1, path, grid, computer)

    wpos = add(pos, West)
    explore_dir(wpos, 3, 4, path, grid, computer)

    epos = add(pos, East)
    explore_dir(epos, 4, 3, path, grid, computer)    

def print_grid(grid):
    os.system('clear')
    minx = min(map(lambda k: k[0], grid.keys()))
    maxx = max(map(lambda k: k[0], grid.keys()))
    miny = min(map(lambda k: k[1], grid.keys()))
    maxy = max(map(lambda k: k[1], grid.keys()))
    for y in range(miny, maxy+1):
        s = ''
        for x in range(minx, maxx+1):
            if (x, y) not in grid:
                s += ' '
            elif x == 0 and y == 0:
                s += 'S'
            else:
                s += grid[(x,y)]
        print(s)
    time.sleep(0.02)
    
def part1():
    computer = Intcode(lines[0])
    grid = defaultdict(int)
    start = (0, 0)
    explore(start, [], grid, computer)
    grid_grid = Grid(grid)
    oxygen = grid_grid.find(GOAL)

    path = A_star(start, oxygen, h = lambda p: manhattan_distance(p, oxygen), grid = grid_grid)
    print(len(path) - 1)

def part2():
    computer = Intcode(lines[0])
    
    grid = defaultdict(int)
    start = (0, 0)
    explore(start, [], grid, computer)
    grid_grid = Grid(grid)
    oxygen = grid_grid.find(GOAL)

    # do a bfs starting from the oxygen location, adding all positions from the next generation
    # at each pass, until no more can be added.
    visited = set()
    q = [[oxygen]]
    minutes = 0
    while q:
        generation = q.pop()
        next_gen = []
        for pos in generation:
            visited.add(pos)
            grid_grid[pos] = 'O'
            neighbors = grid_grid.neighbors(pos, cardinal_directions)
            for n in neighbors:
                if n not in visited and grid_grid[n] != WALL:
                    next_gen.append(n)
        if len(next_gen) > 0:
            q.append(next_gen)
        # print_grid(grid_grid)
            minutes += 1

    print(minutes )

runIt(part1, part2)