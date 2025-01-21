# advent-of-code

2023 - missed a few days, going back to it in 2025 now that I have a better grasp of Python

Jan 17 2025:

- Day 10: Figured out a better way to walk around the pipe and look for points that are "inside" and finally solved part 2
- Day 12: Again, it asks for a COUNT, not a SOLUTION!
- Day 13: I think I just hadn't gotten to this last time around. Took some time to "pythonize" the search for reflections, and smudging the mirror was pretty straightforward. The main bug was that I was stopping when I found a reflection line; so if the old reflection was still valid, and showed up before the new reflection, I wouldn't find the new one.
- Day 17: Finally got a working solution for part 1 using a modified Dijkstra, where each (point, facing) tuple is a "node", and neighbors are 1, 2 or 3 steps to the right or the left of each point. That way we won't backtrack, and won't go more than 3 steps in a given direction. Took 231 seconds. Then updated to use A\* modified for (point, facing) and same neighbor logic and took only 10 seconds.
- Day 17 Part 2: Turned out to be pretty easy, just had to parameterize the min/max number of steps to 4-10. Running A\* got the answer in 31 seconds, could probably use some optimization but it worked. Then updated the modified A\* to use a priority queue and brought the runtime down to 2.5 seconds for part 1, 10 seconds for part 2.
- Day 19: Coming back to this now, Part 1 was easy to recreate. Parsing the rules was the trickiest part. Part 2 was a great application of the guideline to only calculate the number of combinations, not to calculate the combinations themselves! Although I had a frustrating bug where I was modifying a copy of the rules but later referencing the original. Simplifying the code helped to track that down, the solution runs in under 2ms.
