2019

The intcode puzzles have been pretty straightforward so far, but it's been fun to have a solution that builds on previous solutions instead of starting fresh each time.

Day 10 (Building an asteroid monitoring/destroying station):

- This one was a little tricky, I started with a brute-force approach of looping through the asteroids; then for each one, find the line from it to each other asteroid, and loop through them _again_ to find any that are on the line, between the two asteroids, and blocking the view. Later I realized that I just had to identify each line by the angle from the asteroid being considered. If multiple asteroids are on a line with that angle, it doesn't matter, it just counts once! I'm pretty rusty on trig so ended up using numpy.arctan2 and flipping the map so that I could compare the angle of the line to the x axis.
- For Part 2, it was a simple update to store the list of asteroids on each angle, and then loop through them and destroy the closest one at each iteration. I got mixed up a bit with how I "flipped" the graph, and had to go counter-clockwise on the flipped version and translate back to the original version, but it worked out!

Day 11 (Painting a space registration on our ship to avoid space jailtime from the space cops):

- This was cool, writing a driver program to call the Intcode machine with inputs and outputs. Pretty straightforward, and luckily my Intcode computer is fully functional!
