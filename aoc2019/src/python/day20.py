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
testInput2 = (
"             Z L X W       C                 \n"
"             Z P Q B       K                 \n"
"  ###########.#.#.#.#######.###############  \n"
"  #...#.......#.#.......#.#.......#.#.#...#  \n"
"  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  \n"
"  #.#...#.#.#...#.#.#...#...#...#.#.......#  \n"
"  #.###.#######.###.###.#.###.###.#.#######  \n"
"  #...#.......#.#...#...#.............#...#  \n"
"  #.#########.#######.#.#######.#######.###  \n"
"  #...#.#    F       R I       Z    #.#.#.#  \n"
"  #.###.#    D       E C       H    #.#.#.#  \n"
"  #.#...#                           #...#.#  \n"
"  #.###.#                           #.###.#  \n"
"  #.#....OA                       WB..#.#..ZH\n"
"  #.###.#                           #.#.#.#  \n"
"CJ......#                           #.....#  \n"
"  #######                           #######  \n"
"  #.#....CK                         #......IC\n"
"  #.###.#                           #.###.#  \n"
"  #.....#                           #...#.#  \n"
"  ###.###                           #.#.#.#  \n"
"XF....#.#                         RF..#.#.#  \n"
"  #####.#                           #######  \n"
"  #......CJ                       NM..#...#  \n"
"  ###.#.#                           #.###.#  \n"
"RE....#.#                           #......RF\n"
"  ###.###        X   X       L      #.#.#.#  \n"
"  #.....#        F   Q       P      #.#.#.#  \n"
"  ###.###########.###.#######.#########.###  \n"
"  #.....#...#.....#.......#...#.....#.#...#  \n"
"  #####.#.###.#######.#######.###.###.#.#.#  \n"
"  #.......#.......#.#.#.#.#...#...#...#.#.#  \n"
"  #####.###.#####.#.#.#.#.###.###.#.###.###  \n"
"  #.......#.....#.#...#...............#...#  \n"
"  #############.#.#.###.###################  \n"
"               A O F   N                     \n"
"               A A D   M                     \n")


input = PuzzleInput('input/day20.txt', testInput2)

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

def is_outer_portal(p: Point, grid: Grid) -> bool:
    return p[0] == 0 or p[0] == grid.size[0] or p[1] == 0 or p[1] == grid.size[1]

# Use a differently modified A* where the nodes are a tuple of grid point and level, and
# portals move between levels.
def solve_part2(start_pos: Point, grid: Grid, portals: dict[str, set[Point]]):
    goal_pos = list(portals['ZZ'])[0]
    goal = (goal_pos, 0)
    print(f'Goal: {goal}')

    start = (start_pos, 0)
    print(f'From {start}')

    # create a dict to lookup portals by their positions
    portals_by_pos = dict()
    for k,v in portals.items():
        for p in v:
            portals_by_pos[p] = k

    # estimate based on manhattan distance * the level to encourage going back to level 0
    def h(p):
        return manhattan_distance(p[0], goal[0]) * (p[1] + 1)

    openSet = []
    heappush(openSet,(h(start), start))

    cameFrom: dict[tuple[int, int, int], Point] = dict()

    # For node n, gScore[n] is the currently known cost of the cheapest path from start to n.
    gScore: dict[tuple[int, int, int], int]  = defaultdict(lambda: sys.maxsize)
    gScore[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore: dict[tuple[int, int, int], int] = defaultdict(lambda: sys.maxsize)
    fScore[start] = h(start)

    while len(openSet) > 0:
        (priority, current) = heappop(openSet)
        
        neighbors = [(n, current[1]) for n in [add(current[0], d) for d in cardinal_directions] if n in grid and grid[n] == '.']
        if current[0] in portals_by_pos:
            portal_name = portals_by_pos[current[0]]
            outer = is_outer_portal(current[0], grid)
            if (outer and current[1] > 0) or not outer:
                portal = portals[portal_name]
                other = portal.difference({current[0]})
                if len(other) > 0:
                    exit = other.pop()
                    level = current[1] - 1 if outer else current[1] + 1
                    if level <= 25:
                        neighbors.append((exit, level))

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
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
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
    result = solve_part2(start, grid, portals)
    print(result)

runIt(part1, part2)
