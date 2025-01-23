from collections import deque
from typing import Set, Tuple
from aoc_utils import runIt, PuzzleInput, Grid, Point, add, North, South, East, West, cardinal_directions
import numpy as np
import functools
import math
import re
import itertools
import sys

testInput = r"""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
input = PuzzleInput('input-day21.txt', testInput)
lines = input.getInputLines(test=False)

def part1():
    grid = Grid(lines)
    start = grid.find('S')
    grid[start] = '.'

    stepGoal = 64
    q = {start}

    for i in range(stepGoal):
        stepq = list(q)
        q = set()
        while len(stepq) > 0:
            step = stepq.pop()
            q.update(n for n in grid.neighbors(step) if grid[n] == '.')
    
    print(f'Hit {len(q)}')


def part2():
    grid = lines # Grid(lines)
    # start = grid.find('S')
    # grid[start] = '.'

    stepGoal =  26_501_365
    m = len(grid) # grid.size[0]
    n = len(grid[0]) # grid.size[1]


# found various explanations of using the quadratic formula to solve this on Reddit:
# https://www.reddit.com/r/adventofcode/comments/18nevo3/2023_day_21_solutions/
# Took some time to finally understand it.

# This code is from from https://github.com/mgtezak/Advent_of_Code/blob/master/2023/Day_21.py
    # After having crossed the border of the first grid, all further border crossings are seperated by n steps (length/width of grid)
    # Therefore, the total number of grids to traverse in any direction is 26_501_365 // n = x_final
    # Assumption: at step 26_501_365 another border crossing is taking place
    # If so, then it follows that the first crossing takes place at 26_501_365 % n = remainder
    x_final, remainder = divmod(stepGoal, n)
    border_crossings = [remainder, remainder + n, remainder + 2*n]

    visited = set()
    queue = deque([(n//2, n//2)])
    total = [0, 0]  # [even, odd]
    Y = []
    for step in range(1, border_crossings[-1]+1):
        for _ in range(len(queue)):
            x, y = queue.popleft()
            for i, j in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if (i, j) in visited or grid[i%m][j%n] == '#':
                    continue

                visited.add((i, j))
                queue.append((i, j))
                total[step % 2] += 1

        if step in border_crossings:
            Y.append(total[step % 2])

    print(Y)
    print(total)
    X = [0, 1, 2]
    coefficients = np.polyfit(X, Y, deg=2)      # get coefficients for quadratic equation y = a*x^2 + bx + c
    y_final = np.polyval(coefficients, x_final) # using coefficients, get y value at x_final
    answer = math.ceil(y_final) # Have to round UP! y_final.round().astype(int)


    # 627960775905777 
    print(f'part 2 answer: {answer}')

runIt(part1, part2)


"""
26501365 - 65 = 26501299
stammt@Mac aoc2023 %  cd /Users/stammt/Documents/dev/advent-of-code/aoc2023 ; /usr/bin/env /usr/local/bin/python3 /Users/stammt/.vscode/extensions/ms-python.debug
py-2024.14.0-darwin-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 61548 -- /Users/stammt/Documents/dev/advent-of-code/aoc2023/day21.py 
Hit 3768
Step 66 Got to grid at x 1
Step 66 got to y 1
Grid (0, 0) now full at step 129 after 129 steps, started with {(65, 65)}
Step 197 Got to grid at x 2
Step 197 got to y 2
Grid (0, -1) now full at step 260 after 194 steps, started with {(65, 130)}
Grid (-1, 0) now full at step 260 after 194 steps, started with {(130, 65)}
Grid (1, 0) now full at step 260 after 194 steps, started with {(0, 65)}
Grid (0, 1) now full at step 260 after 194 steps, started with {(65, 0)}
Step 328 Got to grid at x 3
Step 328 got to y 3
Grid (1, 1) now full at step 380 after 248 steps, started with {(0, 0)}
Grid (0, -2) now full at step 391 after 194 steps, started with {(65, 130)}
Grid (-1, -1) now full at step 391 after 259 steps, started with {(130, 130)}
Grid (1, -1) now full at step 391 after 259 steps, started with {(0, 130)}
Grid (-2, 0) now full at step 391 after 194 steps, started with {(130, 65)}
Grid (2, 0) now full at step 391 after 194 steps, started with {(0, 65)}
Grid (-1, 1) now full at step 391 after 259 steps, started with {(130, 0)}
Grid (0, 2) now full at step 391 after 194 steps, started with {(65, 0)}
Step 459 Got to grid at x 4
Step 459 got to y 4
Grid (2, 1) now full at step 511 after 248 steps, started with {(0, 0)}
Grid (1, 2) now full at step 511 after 248 steps, started with {(0, 0)}
Grid (0, -3) now full at step 522 after 194 steps, started with {(65, 130)}
Grid (-1, -2) now full at step 522 after 259 steps, started with {(130, 130)}
Grid (1, -2) now full at step 522 after 259 steps, started with {(0, 130)}
Grid (-2, -1) now full at step 522 after 259 steps, started with {(130, 130)}
Grid (2, -1) now full at step 522 after 259 steps, started with {(0, 130)}
Grid (-3, 0) now full at step 522 after 194 steps, started with {(130, 65)}
Grid (3, 0) now full at step 522 after 194 steps, started with {(0, 65)}
Grid (-2, 1) now full at step 522 after 259 steps, started with {(130, 0)}
Grid (-1, 2) now full at step 522 after 259 steps, started with {(130, 0)}
Grid (0, 3) now full at step 522 after 194 steps, started with {(65, 0)}
Step 590 Got to grid at x 5
Step 590 got to y 5
Grid (3, 1) now full at step 642 after 248 steps, started with {(0, 0)}
Grid (2, 2) now full at step 642 after 248 steps, started with {(0, 0)}
Grid (1, 3) now full at step 642 after 248 steps, started with {(0, 0)}
Grid (0, -4) now full at step 653 after 194 steps, started with {(65, 130)}
Grid (-1, -3) now full at step 653 after 259 steps, started with {(130, 130)}
Grid (1, -3) now full at step 653 after 259 steps, started with {(0, 130)}
Grid (-2, -2) now full at step 653 after 259 steps, started with {(130, 130)}
Grid (2, -2) now full at step 653 after 259 steps, started with {(0, 130)}
Grid (-3, -1) now full at step 653 after 259 steps, started with {(130, 130)}
Grid (3, -1) now full at step 653 after 259 steps, started with {(0, 130)}
Grid (-4, 0) now full at step 653 after 194 steps, started with {(130, 65)}
Grid (4, 0) now full at step 653 after 194 steps, started with {(0, 65)}
Grid (-3, 1) now full at step 653 after 259 steps, started with {(130, 0)}
Grid (-2, 2) now full at step 653 after 259 steps, started with {(130, 0)}
Grid (-1, 3) now full at step 653 after 259 steps, started with {(130, 0)}
Grid (0, 4) now full at step 653 after 194 steps, started with {(65, 0)}
Step 721 Got to grid at x 6
Step 721 got to y 6
stammt@Mac aoc2023 % """