from collections import defaultdict
from functools import cache
from heapq import heappop, heappush
import sys
from aoc_utils import PuzzleInput, add, reconstruct_path, runIt, Point, manhattan_distance, Grid, cardinal_directions
from itertools import count, permutations
from numpy import arctan, arctan2, pi
import math

# 23
testInput1 = ("""         A           \n"""
"""         A           \n"""
"""  #######.#########  \n"""
"""  #######.........#  \n"""
"""  #######.#######.#  \n"""
"""  #######.#######.#  \n"""
"""  #######.#######.#  \n"""
"""  #####  B    ###.#  \n"""
"""BC...##  C    ###.#  \n"""
"""  ##.##       ###.#  \n"""
"""  ##...DE  F  ###.#  \n"""
"""  #####    G  ###.#  \n"""
"""  #########.#####.#  \n"""
"""DE..#######...###.#  \n"""
"""  #.#########.###.#  \n"""
"""FG..#########.....#  \n"""
"""  ###########.#####  \n"""
"""             Z       \n"""
"""             Z       \n""")

# for part 2, recursive: 396
testInput2 = ("             Z L X W       C                 "
"             Z P Q B       K                 "
"  ###########.#.#.#.#######.###############  "
"  #...#.......#.#.......#.#.......#.#.#...#  "
"  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  "
"  #.#...#.#.#...#.#.#...#...#...#.#.......#  "
"  #.###.#######.###.###.#.###.###.#.#######  "
"  #...#.......#.#...#...#.............#...#  "
"  #.#########.#######.#.#######.#######.###  "
"  #...#.#    F       R I       Z    #.#.#.#  "
"  #.###.#    D       E C       H    #.#.#.#  "
"  #.#...#                           #...#.#  "
"  #.###.#                           #.###.#  "
"  #.#....OA                       WB..#.#..ZH"
"  #.###.#                           #.#.#.#  "
"CJ......#                           #.....#  "
"  #######                           #######  "
"  #.#....CK                         #......IC"
"  #.###.#                           #.###.#  "
"  #.....#                           #...#.#  "
"  ###.###                           #.#.#.#  "
"XF....#.#                         RF..#.#.#  "
"  #####.#                           #######  "
"  #......CJ                       NM..#...#  "
"  ###.#.#                           #.###.#  "
"RE....#.#                           #......RF"
"  ###.###        X   X       L      #.#.#.#  "
"  #.....#        F   Q       P      #.#.#.#  "
"  ###.###########.###.#######.#########.###  "
"  #.....#...#.....#.......#...#.....#.#...#  "
"  #####.#.###.#######.#######.###.###.#.#.#  "
"  #.......#.......#.#.#.#.#...#...#...#.#.#  "
"  #####.###.#####.#.#.#.#.###.###.#.###.###  "
"  #.......#.....#.#...#...............#...#  "
"  #############.#.#.###.###################  "
"               A O F   N                     "
"               A A D   M                     ")


input = PuzzleInput('input/day20.txt', testInput1)

lines = input.getInputLines(test=False, strip=False)



def solve_part1_astar(start_pos: Point, grid: Grid, portals: dict[str, set[Point]]):
    goal = list(portals['ZZ'])[0]

    # create a dict to lookup portals by their positions
    portals_by_pos = dict()
    for k,v in portals.items():
        for p in v:
            portals_by_pos[p] = k

    def h(p):
        return manhattan_distance(p, goal)

    openSet = []
    heappush(openSet,(h(start_pos), start_pos))

    cameFrom: dict[tuple[int, int, int], Point] = dict()

    # For node n, gScore[n] is the currently known cost of the cheapest path from start to n.
    gScore: dict[tuple[int, int, int], int]  = defaultdict(lambda: sys.maxsize)
    gScore[start_pos] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore: dict[tuple[int, int, int], int] = defaultdict(lambda: sys.maxsize)
    fScore[start_pos] = h(start_pos)

    while len(openSet) > 0:
        (priority, current) = heappop(openSet)
        
        neighbors = [n for n in [add(current, d) for d in cardinal_directions] if n in grid and grid[n] == '.']
        if current in portals_by_pos:
            portal_name = portals_by_pos[current]
            portal = portals[portal_name]
            other = portal.difference({current})
            if len(other) > 0:
                exit = other.pop()
                neighbors.append(exit)

        for n in neighbors:
            tentative_gScore = gScore[current] + 1
            if tentative_gScore < gScore[n]:
                cameFrom[n] = current
                gScore[n] = tentative_gScore
                fScore[n] = tentative_gScore + h(n)
                if n not in openSet:
                    heappush(openSet, (fScore[n], n))

    return gScore[goal]

def parse_input() -> tuple[Grid, dict[str,set[Point]]]:
    # Find the first and last rows of the donut hole
    # Parse out the grid, skipping 2 chars on all sides for the portal names
    x_start = 2
    x_end = len(lines[0]) - 2
    y_start = 2
    y_end = len(lines) - 2
    # hole start/end relative to the full lines
    hole_start_y = -1
    hole_end_y = -1
    hole_start_x = -1
    hole_end_x = -1

    in_hole = False
    for y in range(y_start, y_end):
        # print(lines[y])
        s = lines[y]
        x1 = s.find(' ', 2, -2)
        if not in_hole and x1 > -1:
            hole_start_y = y
            hole_start_x = x1
            hole_end_x = s.rfind(' ', x1, -2)
            in_hole = True
        elif in_hole and x1 == -1:
            hole_end_y = y-1
            in_hole = False

    grid_dict = defaultdict(lambda: ' ')
    for y in range(y_start, y_end+1):
        for x in range(x_start, x_end+1):
            if y >= hole_start_y and y <= hole_end_y and x >= hole_start_x and x <= hole_end_x:
                grid_dict[(x-x_start, y-y_start)] = ' '
            else:
                grid_dict[(x-x_start,y-y_start)] = lines[y][x]

    grid = Grid(grid_dict)

    # Now find the portals
    # top and bottom row, and top and bottom of hole
    portals = defaultdict(set)
    for x in range(x_start, x_end+1):
        if lines[0][x] != ' ':
            portals[f'{lines[0][x]}{lines[1][x]}'].add((x-x_start,0))
        if lines[y_end][x] != ' ':
            portals[f'{lines[y_end][x]}{lines[y_end+1][x]}'].add((x-x_start,y_end-y_start-1))
        if x >= hole_start_x and x <= hole_end_x:
            if lines[hole_start_y][x] != ' ':
                portals[f'{lines[hole_start_y][x]}{lines[hole_start_y+1][x]}'].add((x-x_start,hole_start_y-y_start-1))
            if lines[hole_end_y][x] != ' ':
                portals[f'{lines[hole_end_y-1][x]}{lines[hole_end_y][x]}'].add((x-x_start,hole_end_y-y_start+1))

    for y in range(y_start, y_end+1):
        if lines[y][0] != ' ':
            portals[f'{lines[y][0]}{lines[y][1]}'].add((0,y-y_start))
        if lines[y][x_end] != ' ':
            portals[f'{lines[y][x_end]}{lines[y][x_end+1]}'].add((x_end-x_start-1,y-y_start))
        if y >= hole_start_y and y <= hole_end_y:
            if lines[y][hole_start_x] != ' ':
                portals[f'{lines[y][hole_start_x]}{lines[y][hole_start_x+1]}'].add((hole_start_x-x_start-1,y-y_start))
            if lines[y][hole_end_x] != ' ':
                portals[f'{lines[y][hole_end_x-1]}{lines[y][hole_end_x]}'].add((hole_end_x-x_start+1,y-y_start))

    return (grid, portals)

def part1():
    grid, portals = parse_input()
    start = list(portals['AA'])[0]
    print(f'Starting at {start}')
    result = solve_part1_astar(start, grid, portals)
    print(result)

def part2():
    grid, portals = parse_input()
    start = list(portals['AA'])[0]
    print(f'Starting at {start}')
    # TODO: update to solve recursive maze
    result = solve_part1_astar(start, grid, portals)
    print(result)

runIt(part1, part2)
