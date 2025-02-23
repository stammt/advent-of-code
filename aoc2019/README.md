2019

The intcode puzzles have been pretty straightforward so far, but it's been fun to have a solution that builds on previous solutions instead of starting fresh each time.

Day 10 (Building an asteroid monitoring/destroying station):

- This one was a little tricky, I started with a brute-force approach of looping through the asteroids; then for each one, find the line from it to each other asteroid, and loop through them _again_ to find any that are on the line, between the two asteroids, and blocking the view. Later I realized that I just had to identify each line by the angle from the asteroid being considered. If multiple asteroids are on a line with that angle, it doesn't matter, it just counts once! I'm pretty rusty on trig so ended up using numpy.arctan2 and flipping the map so that I could compare the angle of the line to the x axis.
- For Part 2, it was a simple update to store the list of asteroids on each angle, and then loop through them and destroy the closest one at each iteration. I got mixed up a bit with how I "flipped" the graph, and had to go counter-clockwise on the flipped version and translate back to the original version, but it worked out!

Day 11 (Painting a space registration on our ship to avoid space jailtime from the space cops):

- This was cool, writing a driver program to call the Intcode machine with inputs and outputs. Pretty straightforward, and luckily my Intcode computer is fully functional!

Day 12 (That's no moon!)

- Part 1 was pretty straightforward, I spent some time collapsing nested for-loops into python list generators just for fun...
- Part 2 took a while. I had a feeling it was about finding the length of the cycles where positions repeated, and then finding the LCM, but I had trouble getting it exactly right. My first attempt worked for the small sample but not the larger one; then I eventually realized that (a) I had to compare the x,y,z, separately and not compare the moons separately, and (b) I had to start with step 1, not 0! I had been starting with 0 and then adding 1 at the end, but this doesn't give the right cycle step counts.

Day 13 (Pong)

- This one was awesome, another intcode arcade game! I think Part 1 was just to verify the machine. For Part 2 I did some experimentation to see how the ball moved, then realized the driver code just needed to be a simple reaction to "chase" the ball as it moved - go right if it's moving right, and left if it's moving left. After getting the answer I did some simple ansi drawing code to create an ascii animation of the game :)

Day 14 (Mining ore for fuel)

- I feel like Part 1 should have been simple but I got tripped up on managing "leftover" resources. Several times my solution worked for some samples, but not others. Eventually I got it right though...
- Part 2 took some experimentation. For the sample I could just run the mining code in a loop to get to 1 trillion ore, but that didn't work for the real input. I had a few false starts around looking for a loop in the processing (e.g. passing the leftover resources over and over to see if I got back to the initial state). After leaving it alone overnight I realized that instead of trying to make 1 FUEL and vary the amount of ore, I should keep the amount of ore steady and vary the amount of FUEL to make in a single call. Doing that in a binary search for the max amount of fuel I could request got the right answer!

Day 15 (Oxygen repair)

- Another intcode problem! For part 1 I wrote a simple dfs to discover the grid by testing each direction and then backtracking to the known start location when I hit a dead end. This worked well, and then I was able to use A\* search to find the shortest path to the oxygen processor.
- Part 2 was also pretty straightforward, just do a breadth-first traversal to see how man loops it would take to fill the empty part of the grid with oxygen. The only tricky bit was to track the progress per "generation" rather than each individual expansion, since it's expanding in all directions every minute.

Day 16 ()

Day 17 (Moving the cleaning robot)

- Part 1 was simple, just parsing the intcode output into a grid and finding the path intersections
- I "cheated" a little bit on part 2, I wrote quick function to simply follow all the turns of the path, and then output the commands that it would have used in the format "turn", "number of steps". After staring at the commands for a few minutes I figured out the three repeating subroutines and just hardcoded them in the program. It worked! I was sure it wouldn't just be the "simple" path so I was trying to figure out how to find all the different paths, but I guess I was over-thinking it. It wouldn't be too hard to write code to find the repeating subroutines, but... I don't have to :)

Day 18 (Find the keys and unlock the doors!)

- Part 1: Whoa, this one took a while. I had a lot of different approaches that worked on most of the samples but took much too long on the last one, and never finished on the real input data. Most of them ended up testing every possible path, either through a dfs or bfs, or by trying all permutations of the keys that were valid. I finally looked up some hints on reddit and was able to use A\* to solve it by treating each point in the grid as x,y,keys using a bitmask of which keys had been collected. (a set worked too but was much slower) The shortest "path" to a node where we have collected all of the keys gives the number of steps.
- Part 2: After getting part 1, this wasn't too bad. Inside of the A\* loop I had each bot move individually, and each "node" was the combination of bot positions and collected keys. This worked on all of the test data but was too slow on the real input (stopped afer >30 minutes). I made an optimization to treat accessible keys as neighbors instead of moving one point at a time, and that ran in under a minute! I added the same optimization to part 1 and now it runs in 18 seconds (down from hours+).

Day 19 (Tractor beam for santa)

- Part 1: Simple use of Intcode again. Got a little mixed up because instead of taking input over and over, this machine needs to be reset between queries, but otherwise it was trivial.
- Part 2: I outsmarted myself here, tried to find the slope of the lines defining the beam and then figure out where the box would fit. Unfortunately finding the slopes didn't really work because it was already quantized to the grid, so I ended up with a result that was close but not exact. Finally realized I could just "walk down" the top of the beam and check the bounding corners of the 100x100 box at each point to see where it would fit. I guess you could do a binary search here to make it even faster, but... _shrug_

Day 20 (The recursive portal maze)

- Part 1: After a ton of off-by-one errors in parsing, the actual solution was pretty easy! Just used a modified A\* to count portal exits as neighbors. I wasn't able to short-circuit when hitting the goal because I didn't have a legit h function to estimate the priority, but it still ran in less than 15ms.
- Part 2: Turns out I still had an off-by-one error in the parsing, which threw off my check for whether or not a portal was on the outer or inner side of the grid. Once I got that straightened out it wasn't too hard to adapt the A\* algorithm to traverse levels, although with the "inifinite" size I had to put in an arbitrary constraint on the number of levels to try. Also updated the heuristic to estimate distance to take into account the level to try to encourage going back to level 0. It worked!

Day 21 (Walk before you run)

- Part 1: took some trial and error to figure out the logic, but eventually was able to handle enough cases that I got a result.
- Part 2: this was really an extension of part 1, and I guess my logic from part 1 was pretty good because I only had to tweak it a little bit to get a result.
