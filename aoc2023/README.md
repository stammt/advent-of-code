# advent-of-code

2023 - missed a few days, going back to it in 2025 now that I have a better grasp of Python

Jan 17 2025:

- Day 10: Figured out a better way to walk around the pipe and look for points that are "inside" and finally solved part 2
- Day 12: Again, it asks for a COUNT, not a SOLUTION!
- Day 13: I think I just hadn't gotten to this last time around. Took some time to "pythonize" the search for reflections, and smudging the mirror was pretty straightforward. The main bug was that I was stopping when I found a reflection line; so if the old reflection was still valid, and showed up before the new reflection, I wouldn't find the new one.
- Day 17: Finally got a working solution for part 1 using a modified Dijkstra, where each (point, facing) tuple is a "node", and neighbors are 1, 2 or 3 steps to the right or the left of each point. That way we won't backtrack, and won't go more than 3 steps in a given direction.
