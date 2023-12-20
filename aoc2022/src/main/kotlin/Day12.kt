import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day12input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day11sample.txt").readLines()
//    val input = mutableListOf<String>(
//        "Sabqponm",
//        "abcryxxl",
//        "accszExk",
//        "acctuvwj",
//        "abdefghi"
//    )
    day12part2(input)
}

fun day12part2(input: List<String>) {
    val startLoc = findStart(input)

    val visited = mutableSetOf<Pair<Int, Int>>()

    val distances = mutableMapOf<Pair<Int, Int>, Int>()
    distances[startLoc] = 0

    findShortestPath(input, visited, distances)

    // find the node with height 'a' with the shortest distance
    var shortest = Int.MAX_VALUE
    for (y in input.indices) {
        for (x in input[y].indices) {
            if (distances.containsKey(x to y) && realHeight(input[y][x]) == 'a') {
                val dist = distances[x to y]!!
                shortest = min(shortest, dist)
            }
        }
    }

    println("result: $shortest")
}

fun day12part1(input: List<String>) {
    val startLoc = findStart(input)

    val visited = mutableSetOf<Pair<Int, Int>>()

    val distances = mutableMapOf<Pair<Int, Int>, Int>()
    distances[startLoc] = 0

    val distance = findShortestPath(input, visited, distances)

    println("result: $distance")
}

fun findShortestPath(input: List<String>, visited: MutableSet<Pair<Int, Int>>, distances: MutableMap<Pair<Int, Int>, Int>) : Int {
    while (distances.entries.filterNot { visited.contains(it.key) }.isNotEmpty()) {
        val u = distances.entries.filterNot { visited.contains(it.key) }.minBy { it.value }
//        println("checking node ${u.key} with height ${input[u.key.second][u.key.first]} and dist ${u.value}")
        visited.add(u.key)
//        if (input[u.key.second][u.key.first] == 'E') {
//            return u.value
//        }

        val height = input[u.key.second][u.key.first]
        val steps = getChildren(input, u.key)
//        println("Found ${steps.size} steps from ${u.key} : $steps")
        for (step in steps) {
            val alt = u.value + 1
            if (!distances.containsKey(step) || alt < distances[step]!!) {
                distances[step] = alt
            }
        }
    }
    println("Never found the end!")
    return -1
}

fun findStart(input: List<String>) : Pair<Int, Int> {
    for (y in input.indices) {
        val x = input[y].indexOf('E')
        if (x != -1) {
            return x to y
        }
    }
    throw IllegalArgumentException("No start node found")
}

fun getChildren(input: List<String>, loc: Pair<Int, Int>) : List<Pair<Int, Int>> {
    val height = realHeight(input[loc.second][loc.first])
    val children = mutableListOf<Pair<Int, Int>>()
    if (loc.first > 0 && canStep(height, realHeight(input[loc.second][loc.first - 1]))) {
        children.add(loc.first - 1 to loc.second)
    }
    if (loc.first < input[0].length-1 && canStep(height, realHeight(input[loc.second][loc.first + 1]))) {
        children.add(loc.first + 1 to loc.second)
    }
    if (loc.second > 0 && canStep(height, realHeight(input[loc.second - 1][loc.first]))) {
        children.add(loc.first to loc.second-1 )
    }
    if (loc.second < input.size-1 && canStep(height, realHeight(input[loc.second + 1][loc.first]))) {
        children.add(loc.first to loc.second+1 )
    }
    return children
}

fun canStep(fromHeight: Char, toHeight: Char) : Boolean {
//    return toHeight <= (fromHeight + 1)
    return toHeight >= (fromHeight - 1) // going backwards
}

fun realHeight(height: Char) : Char {
    return if (height == 'S') 'a' else if (height == 'E') 'z' else height
}

