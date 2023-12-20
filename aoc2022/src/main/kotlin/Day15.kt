import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day15input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day15sample.txt").readLines()
//    val input = listOf(
//        "498,4 -> 498,6 -> 496,6",
//        "503,4 -> 502,4 -> 502,9 -> 494,9"
//    )
    day15part2(input)
}

// Part 1: query each sensor for the points covered in the row, and subtract the beacons in that row
// Part 2: for each row, find the range of points covered by each beacon. Sort the ranges
//         by starting point and merge them together. If we find a gap, that's the missing spot.

data class Sensor(val point: Pair<Int, Int>, val beacon: Pair<Int, Int>) {
    private val range = distance(point, beacon)

    fun isInRange(other: Pair<Int, Int>) : Boolean {
        return distance(point, other) <= range
    }

    fun coveredPointsInRow(y: Int) : Set<Pair<Int, Int>> {
        val yDist = abs(point.second - y)
        val xMax = range - yDist
        val points = mutableSetOf<Pair<Int, Int>>()
        for (x in (point.first-xMax)..(point.first+xMax)) {
            points.add(x to y)
        }

        return points
    }

    fun coveredXInRow(y: Int) : IntRange? {
        val yDist = abs(point.second - y)
        val xDist = range - yDist
        if (xDist < 1) return null
        return IntRange(point.first - xDist, point.first + xDist)
    }

    private fun distance(a: Pair<Int, Int>, b: Pair<Int, Int>) : Int {
        return abs(a.first - b.first) + abs(a.second - b.second)
    }

}

fun day15part2(input: List<String>) {
    val sensors = parseSensors(input)
    var result: Pair<Int, Int>? = null

    val min = 0
    val max = 4000000

    for (y in min..max) {
        if (y % 1000000 == 0) {
            println("Checking row $y")
        }
        val covered = mutableSetOf<IntRange>()
        for (sensor in sensors) {
            val range = sensor.coveredXInRow(y)
            if (range != null) {
                covered.add(range)
            }
        }
        covered.removeIf { it.last < min || it.first > max }

        // merge the ranges and if we find a gap, that's the missing spot
        val sortedRanges = covered.sortedBy { it.first }
        var start = sortedRanges[0].first
        var end = sortedRanges[0].last
        for (range in sortedRanges.drop(1)) {
            if (range.first > end) {
                result = end + 1 to y
                break
            } else {
                end = max(end, range.last)
            }
        }
        if (result != null) {
            break
        }
    }

    val freq = (result!!.first.toLong() * 4000000L) + result!!.second.toLong()

    println("result: $freq from  $result")
}


fun day15part1(input: List<String>) {
    val sensors = parseSensors(input)
    val points = mutableSetOf<Pair<Int, Int>>()
    val y = 2000000

    // add all points covered by sensors in this row
    for (sensor in sensors) {
        points.addAll(sensor.coveredPointsInRow(y))
    }

    // remove all points that are known beacons
    for (sensor in sensors) {
        points.remove(sensor.beacon)
    }

    println("Covered: ${points.size}")
}

fun parseSensors(input: List<String>) : MutableSet<Sensor> {
    val sensors = mutableSetOf<Sensor>()

    for (line in input) {
        val parts = line.split(":").map { it.trim() }

        val sensorPoint = parts[0].substring("Sensor at ".length).trim().split(", ")
            .map { it.substring(2).toInt() }
        val beaconPoint = parts[1].substring("closest beacon is at ".length).trim().split(", ")
            .map { it.substring(2).toInt() }

        sensors.add(Sensor(sensorPoint[0] to sensorPoint[1], beaconPoint[0] to beaconPoint[1]))
    }
    return sensors
}