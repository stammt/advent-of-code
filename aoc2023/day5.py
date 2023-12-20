import sys

input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
# lines = list(map(lambda x: x.strip(), input.splitlines()))

f = open('input-day5.txt', 'r')
lines = list(map(lambda x: x.strip(), f.readlines()))

def splitInts(line):
    return list(map(lambda c: int(c), line.strip().split()))

class RangeMap:
    def __init__(self, mappingStr):
        mapping = splitInts(mappingStr)
        self.dstRange = range(mapping[0], mapping[0] + mapping[2])
        self.srcRange = range(mapping[1], mapping[1] + mapping[2])

    # Returns a list of remaining seed ranges to test, and a destination range from this one
    def getDestRange(self, seedRange):
        # look for an overlap between the seed range and the source range
        intersection = range(max(seedRange.start, self.srcRange.start), min(seedRange.stop, self.srcRange.stop))

        if len(intersection) > 0:
            # extract the intersection from the seed range, and track any leftovers from the
            # start and end
            leftovers = []
            if intersection.start > seedRange.start:
                leftovers.append(range(seedRange.start, intersection.start))
            if intersection.stop < seedRange.stop:
                leftovers.append(range(intersection.stop, seedRange.stop))

            # the destination range
            destinationStart = self.dstRange.start + intersection.start - self.srcRange.start
            seedDestination = range(destinationStart, destinationStart + len(intersection))

            return (seedDestination, leftovers)
        else:
            return (None, [seedRange])
        
class RangeMapCollection:
    def __init__(self, dest, rangeMaps):
        self.dest = dest
        self.rangeMaps = rangeMaps

    def getDest(self, srcRanges):
        destRanges = []
        leftovers = srcRanges
        for rangeMap in self.rangeMaps:
            # track ranges that need to be processed after this mapping
            currentLeftovers = []
            for range in leftovers:
                (dest, resultLeftovers) = rangeMap.getDestRange(range)
                currentLeftovers = currentLeftovers + resultLeftovers
                if dest != None:
                    destRanges.append(dest)
            leftovers = currentLeftovers

        # for any unhandled src ranges, add them to the destination ranges as-is
        return destRanges + leftovers


seedRanges = []
maps = {}
for i in range(len(lines)):
    if lines[i].startswith('seeds: '):
        # seeds = splitInts(lines[i][len('seeds: '):])
        seedPairs = splitInts(lines[i][len('seeds: '):])
        for s in range(0, len(seedPairs), 2):
            seedStart = seedPairs[s]
            seedLen = seedPairs[s+1]
            seedRanges.append([range(seedStart, seedStart + seedLen)])
        print(f'all seed ranges: {seedRanges}')
        i+=1
    elif lines[i].endswith('map:'):
        mapName = lines[i].split()[0]
        source, dash, dest = mapName.split('-')
        currentMaps = []
        i+=1
        while i < len(lines) and len(lines[i].strip()) != 0:
            currentMaps.append(RangeMap(lines[i].strip()))
            i+=1

        maps[source] = RangeMapCollection(dest, currentMaps)

# print(f'Seeds: {seeds}')
# print(f'Maps: {maps}')

minVal = sys.maxsize
for seed in seedRanges:
    sourceName = 'seed'
    sourceValue = seed
    while sourceName != 'location':
        nextMap = maps[sourceName]
        destValue = nextMap.getDest(sourceValue)
        destName = nextMap.dest
        print(f'Mapped {sourceName} {sourceValue} to {destName} {destValue}')

        sourceValue = destValue
        sourceName = destName

    minVal = min(minVal, min(map(lambda x: x.start, destValue)))


print(f'minValue: {minVal}')

            


        
