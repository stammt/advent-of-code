import aoc_utils
from itertools import count

testInput = r""""""
input = aoc_utils.PuzzleInput('input/day08.txt', testInput)

lines = input.getInputLines(test=False)

image_width = 25
image_height = 6

def part1():
    image = list(map(int, lines[0]))
    layer_len = image_width * image_height
    layers = [image[i:i+layer_len] for i in range(0, len(image), layer_len)]

    layers.sort(key = lambda x : x.count(0))
    ones = layers[0].count(1)
    twos = layers[0].count(2)
    
    print(ones * twos)

def part2():
    image = list(map(int, lines[0]))
    layer_len = image_width * image_height
    layers = [image[i:i+layer_len] for i in range(0, len(image), layer_len)]

    stacked = []
    for i in range(0, layer_len):
        # take the first value that is not transparent (2)
        for layer in layers:
            if layer[i] != 2:
                stacked.append(layer[i])
                break
    
    for y in range(0, image_height):
        s = ''.join(list(map(lambda x: '*' if x == 1 else ' ', stacked[y * image_width:(y + 1) * image_width])))
        print(s)


aoc_utils.runIt(part1, part2)