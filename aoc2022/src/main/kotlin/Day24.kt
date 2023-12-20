import java.io.File
import java.lang.IllegalArgumentException
import java.lang.IllegalStateException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day24input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day24sample.txt").readLines()
    day24part1(input)
}

fun day24part1(input: List<String>) {
    val map = mutableMapOf<Pair<Int, Int>, String>()
    for (y in input.indices) {
        for (x in input[y].indices) {
            if (input[y][x] != '.') {
                map[x to y] = input[y][x].toString()
            }
        }
    }

    val maxX = map.map { it.key.first }.max()
    val maxY = map.map { it.key.second }.max()

    val start = 1 to 0
    val end = maxX - 1 to maxY
    var goal = end
    var state = ValleyState(0, setOf(start), map)
    var end1 = 0
    while (!state.elves.contains(goal)) {
        // Build the next map state
        val nextMap = nextMap(state.map)

        // Find the potential moves for the elves
        val potentialMoves = mutableSetOf<Pair<Int, Int>>()
        for (e in state.elves) {
            potentialMoves.addAll(getPotentialMoves(e, nextMap))
        }

        state = ValleyState(state.steps + 1, potentialMoves, nextMap)
    }

    if (state.elves.contains(goal)) {
        end1 = state.steps
        println("Reached goal in ${state.steps} steps")
    } else {
        println("Ran out of potential states")
    }

    goal = start
    state = ValleyState(0, setOf(end), state.map)
    while (!state.elves.contains(goal)) {
//        printValley(state)
        // Build the next map state
        val nextMap = nextMap(state.map)

        // Find the potential moves for the elves
        val potentialMoves = mutableSetOf<Pair<Int, Int>>()
        for (e in state.elves) {
            potentialMoves.addAll(getPotentialMoves(e, nextMap))
        }
//        println("Back to start step ${state.steps} from ${state.elves} to $potentialMoves")

        state = ValleyState(state.steps + 1, potentialMoves, nextMap)
    }
    var backToStart = 0
    if (state.elves.contains(goal)) {
        backToStart = state.steps
        println("Back to start in ${state.steps} steps")
    } else {
        println("Ran out of potential states")
        return
    }

    goal = end
    state = ValleyState(0, setOf(start), state.map)
    while (!state.elves.contains(goal)) {
        // Build the next map state
        val nextMap = nextMap(state.map)

        // Find the potential moves for the elves
        val potentialMoves = mutableSetOf<Pair<Int, Int>>()
        for (e in state.elves) {
            potentialMoves.addAll(getPotentialMoves(e, nextMap))
        }

        state = ValleyState(state.steps + 1, potentialMoves, nextMap)
    }
    var end2 = 0
    if (state.elves.contains(goal)) {
        end2 = state.steps
        println("Reached goal in ${state.steps} steps")
    } else {
        println("Ran out of potential states")
    }

    println("total steps ${end1 + backToStart + end2}")

}

fun getPotentialMoves(elves: Pair<Int, Int>, map: Map<Pair<Int, Int>, String>) : Collection<Pair<Int, Int>>{
    val maxX = map.map { it.key.first }.max()
    val maxY = map.map { it.key.second }.max()

    val potentialMoves = mutableListOf<Pair<Int, Int>>()
    if (elves.first > 0 && !map.containsKey(elves.first-1 to elves.second)) {
        potentialMoves.add(elves.first-1 to elves.second)
    }
    if (elves.first < maxX-1 && !map.containsKey(elves.first+1 to elves.second)) {
        potentialMoves.add(elves.first+1 to elves.second)
    }
    if (elves.second > 0 && !map.containsKey(elves.first to elves.second-1)) {
        potentialMoves.add(elves.first to elves.second-1)
    }
    if (elves.second < maxY && !map.containsKey(elves.first to elves.second+1)) {
        potentialMoves.add(elves.first to elves.second+1)
    }
    if (!map.containsKey(elves)) {
        potentialMoves.add(elves)
    }
    return potentialMoves
}

fun printValley(state: ValleyState) {
    val maxX = state.map.map { it.key.first }.max()
    val maxY = state.map.map { it.key.second }.max()
    println("=== after steps: $state.steps ===")
    for (y in 0..maxY) {
        for (x in 0..maxX) {
            if (state.elves.contains( x to y)) {
                print('E')
            } else {
                val c = state.map[x to y]
                print(if (c == null) '.' else if (c!!.length > 1) c!!.length else c)
            }
        }
        println()
    }
}

data class ValleyState(val steps: Int, val elves: Set<Pair<Int, Int>>, val map: Map<Pair<Int, Int>, String>)

fun nextMap(map: Map<Pair<Int, Int>, String>) : Map<Pair<Int, Int>, String> {
    val updatedMap = mutableMapOf<Pair<Int, Int>, String>()
    val maxX = map.map { it.key.first }.max()
    val maxY = map.map { it.key.second }.max()
    for (x in 0..maxX) {
        for (y in 0..maxY) {
            if (map.containsKey(x to y)) {
                for (c in map[x to y]!!) {
                    if (c == '>') {
                        var blizzardMove = x + 1 to y
                        if (blizzardMove.first == maxX) {
                            blizzardMove = 1 to y
                        }
                        updatedMap[blizzardMove] = if (updatedMap.containsKey(blizzardMove)) updatedMap[blizzardMove]!! + c else c.toString()
                    } else if (c == '<') {
                        var blizzardMove = x - 1 to y
                        if (blizzardMove.first == 0) {
                            blizzardMove = maxX - 1 to y
                        }
                        updatedMap[blizzardMove] = if (updatedMap.containsKey(blizzardMove)) updatedMap[blizzardMove]!! + c else c.toString()
                    } else if (c == '^') {
                        var blizzardMove = x to y - 1
                        if (blizzardMove.second == 0) {
                            blizzardMove = x to maxY - 1
                        }
                        updatedMap[blizzardMove] = if (updatedMap.containsKey(blizzardMove)) updatedMap[blizzardMove]!! + c else c.toString()
                    } else if (c == 'v') {
                        var blizzardMove = x to y + 1
                        if (blizzardMove.second == maxY) {
                            blizzardMove = x to 1
                        }
                        updatedMap[blizzardMove] = if (updatedMap.containsKey(blizzardMove)) updatedMap[blizzardMove]!! + c else c.toString()
                    } else if (c == '#') {
                        updatedMap[x to y] = "#"
                    }
                }
            }
        }
    }
    return updatedMap
}
