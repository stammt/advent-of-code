import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day14input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day13sample.txt").readLines()
//    val input = listOf(
//        "498,4 -> 498,6 -> 496,6",
//        "503,4 -> 502,4 -> 502,9 -> 494,9"
//    )
    day14part2(input)
}

// build a sparse matrix of blocked points, and add to it with each grain
// for part 1 stop when any grains pass the lowest blocked point
// for part 2 just check that the grain hasn't landed on the floor

fun day14part2(input: List<String>) {
    val blocked = parseRocks(input)
    val lowestBlock = blocked.maxOf { it.second }
    val floor = lowestBlock + 2

    val initialCount = blocked.size

    val start = 500 to 0
    var full = false
    while (!blocked.contains(start)) {
        var grain = start.first to start.second

        while (true) {
            if (grain.second == floor - 1) {
                // it's already on the floor
                blocked.add(grain)
                break
            }

            if (!blocked.contains(grain.first to grain.second + 1)) {
                // fall straight down
                grain = grain.first to grain.second + 1
            } else if (!blocked.contains(grain.first - 1 to grain.second + 1)) {
                // down and to the left
                grain = grain.first - 1 to grain.second + 1
            } else if (!blocked.contains(grain.first + 1 to grain.second + 1)) {
                // down and to the right
                grain = grain.first + 1 to grain.second + 1
            } else {
                // settled!
                blocked.add(grain)
                break
            }
        }
    }

    println("settled: ${blocked.size - initialCount}")
}


fun day14part1(input: List<String>) {
    val blocked = parseRocks(input)
    val lowestBlock = blocked.maxOf { it.second }
    println("Lowest block: $lowestBlock")

    val initialCount = blocked.size

    val start = 500 to 0
    var full = false
    while (!full) {
        var grain = start.first to start.second

        while (true) {
            if (grain.second > lowestBlock) {
                full = true
                break
            } else {
                if (!blocked.contains(grain.first to grain.second + 1)) {
                    // fall straight down
                    grain = grain.first to grain.second + 1
                } else if (!blocked.contains(grain.first - 1 to grain.second + 1)) {
                    // down and to the left
                    grain = grain.first - 1 to grain.second + 1
                } else if (!blocked.contains(grain.first + 1 to grain.second + 1)) {
                    // down and to the right
                    grain = grain.first + 1 to grain.second + 1
                } else {
                    // settled!
                    blocked.add(grain)
                    break
                }
            }
        }
    }

    println("settled: ${blocked.size - initialCount}")
}

fun parseRocks(input: List<String>) : MutableSet<Pair<Int, Int>> {
    val blocked = mutableSetOf<Pair<Int, Int>>()

    for (line in input) {
        val points = line.split(" -> ").map { it.split(',') }.map { it[0].toInt() to it[1].toInt() }
        var lastPoint: Pair<Int, Int>? = null
        for (p in points) {
            blocked.add(p)
            if (lastPoint != null) {
                if (lastPoint.first == p.first) {
                    if (lastPoint.second < p.second) {
                        for (y in lastPoint.second..p.second) {
                            blocked.add(lastPoint.first to y)
                        }
                    } else if (lastPoint.second > p.second) {
                        for (y in p.second..lastPoint.second) {
                            blocked.add(lastPoint.first to y)
                        }
                    }
                } else {
                    if (lastPoint.first < p.first) {
                        for (x in lastPoint.first..p.first) {
                            blocked.add(x to lastPoint.second)
                        }
                    } else if (lastPoint.first > p.first) {
                        for (x in p.first..lastPoint.first) {
                            blocked.add(x to lastPoint.second)
                        }
                    }
                }
            }
            lastPoint = p
        }
    }
    return blocked
}