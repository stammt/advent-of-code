import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day17input.txt").readLines()
//    val input = listOf(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
    day17part1(input.first())
}

// Use a sparse graph to represent where rocks are in the column, moving around
// a "sprite" of the falling rock until it settles and checking for collisions
// by just looking for overlapping pixels.
// Part 1: straightforward, running the algorithm 2022 times is fast
// Part 2: look for repeating cycles by storing the state after each rock settles (the shape
// of the floor along with the last jet and rock). If a state repeats, we can calculate the rest
// of the run as repetitions of the height difference between the original state and the repeat,
// and then drop enough more rocks to hit the target number (cycle size modulo number of rocks).

fun day17part1(input: String) {
    val rockPatterns = generateRocks()
    val column = mutableSetOf<Pair<Long, Long>>()

    // map of column state to (rock count -> height)
    val previousStates = mutableMapOf<ColumnState, Pair<Long, Long>>()
    var calculatedTop: Long? = null
    var topWhenRepeatedStateFound: Long? = null

    val rockCountGoal = 1000000000000L
    var rockPatternIndex = 0
    var jetIndex = 0
    var settledRockCount = 0L
    var lastTop = 0L
    do {
        val lastRock = rockPatternIndex
        val rock = rockPatterns[rockPatternIndex++]
        rockPatternIndex %= rockPatterns.size

        val highestPoint = getHighestPoint(column)
        var rockPos = 2L to highestPoint + 4L

        var isSettled = false
        var lastJet: Int
        do {
            lastJet = jetIndex
            val jet = input[jetIndex++]
            jetIndex %= input.length

            rockPos = jet(jet, rock, rockPos, column)
            val fallPos = fall(rock, rockPos, column)

            if (fallPos == rockPos) {
                settle(rock, rockPos, column)
                isSettled = true
            } else {
                rockPos = fallPos
            }
        } while (!isSettled)

        settledRockCount++

        // if we haven't repeated yet, check to see if we've already seen this state
        if (calculatedTop == null) {
            val floorShape = floorShape(column)
            val state = ColumnState(lastRock, lastJet, floorShape)
            val top = getHighestPoint(column) + 1
            if (previousStates.containsKey(state)) {
                val previousSettledRockCount = previousStates[state]!!.first
                val previousTop = previousStates[state]!!.second
                println("Found repeated state from $previousSettledRockCount with height $previousTop")

                val cycleLength = settledRockCount - previousSettledRockCount
                val cycleHeight = top - previousTop
                println("cycle length $cycleLength with height $cycleHeight")

                val remainingRocks = rockCountGoal - settledRockCount
                val repeatFor = remainingRocks / cycleLength
                calculatedTop = top + (repeatFor * cycleHeight)
                println("Repeated cycle $repeatFor times, now top is $calculatedTop")

                val andAdd = remainingRocks % cycleLength
                println("Need to drop $andAdd more rocks")
                settledRockCount = rockCountGoal - andAdd
                topWhenRepeatedStateFound = top
            } else {
                // Record this state
                previousStates[state] = settledRockCount to top
            }
        }
    } while (settledRockCount < rockCountGoal)

    val top = getHighestPoint(column) + 1

    if (calculatedTop != null && topWhenRepeatedStateFound != null) {
        val remainingHeight = top - topWhenRepeatedStateFound
        val totalCalculatedTop = calculatedTop + remainingHeight
        println("Top with repetitions: $totalCalculatedTop")
    } else {
        println("Top: $top")
    }
}

data class Rock(val points: Set<Pair<Long, Long>>, val width: Int, val height: Int) { }

data class ColumnState(val lastRock: Int, val lastJet: Int, val floorShape: List<Long>) { }

fun floorShape(column: Set<Pair<Long, Long>>) : List<Long> {
    // make an array of heights for each 'x' where the lowest point is 0
    val heights = mutableListOf<Long>()
    for (x in 0L until 7L) {
        val points = column.filter { it.first == x }
        if (points.isEmpty()) {
            heights.add(0)
        } else {
            heights.add(points.maxBy { it.second }.second + 1)
        }
    }
    val min = heights.min()
    return heights.map { it - min }
}

fun collision(rock: Rock, rockPos: Pair<Long, Long>, column: Set<Pair<Long, Long>>) : Boolean {
    // Return true if this rock would collide with a wall, a floor, or a settled rock
    val adjustedRock = rock.points.map { it.first + rockPos.first to it.second + rockPos.second }
    if (adjustedRock.any { it.first < 0 || it.first > 6 || it.second < 0}) return true
    if (adjustedRock.any { column.contains(it) }) return true
    return false
}

fun jet(jet: Char, rock: Rock, rockPos: Pair<Long, Long>, column: Set<Pair<Long, Long>>) : Pair<Long, Long> {
    val afterX = if (jet == '>') rockPos.first + 1 else rockPos.first - 1
    val afterPos = afterX to rockPos.second
    if (collision(rock, afterPos, column)) return rockPos
    return afterPos
}

fun fall(rock: Rock, rockPos: Pair<Long, Long>, column: Set<Pair<Long, Long>>) : Pair<Long, Long> {
    val afterPos = rockPos.first to rockPos.second-1
    if (collision(rock, afterPos, column)) return rockPos
    return afterPos
}

fun settle(rock: Rock, rockPos: Pair<Long, Long>, column: MutableSet<Pair<Long, Long>>) {
    val adjustedRock = rock.points.map { it.first + rockPos.first to it.second + rockPos.second }
    column.addAll(adjustedRock)
}

fun getHighestPoint(column: Collection<Pair<Long, Long>>) : Long {
    return if (column.isNotEmpty()) column.maxBy { it.second }.second else -1
}

fun printColumn(rock: Rock?, rockPos: Pair<Long, Long>?, column: Set<Pair<Long, Long>>) {
    val adjustedRock = rock?.points?.map { it.first + rockPos!!.first to it.second + rockPos!!.second } ?: mutableSetOf()
    val top = max(getHighestPoint(column), getHighestPoint(adjustedRock))

    for (y in top downTo 0L) {
        print('|')
        for (x in 0L..6L) {
            val c = if (column.contains(x to y)) '#' else if (adjustedRock.contains(x to y)) '@' else '.'
            print(c)
        }
        println('|')
    }
    println("+-------+\n")
}

fun generateRocks() : List<Rock> {
    val r1 = mutableSetOf(
        0L to 0L,
        1L to 0L,
        2L to 0L,
        3L to 0L
    )
    val r2 = mutableSetOf(
        1L to 0L,
        0L to 1L,
        1L to 1L,
        2L to 1L,
        1L to 2L
    )
    val r3 = mutableSetOf(
        0L to 0L,
        1L to 0L,
        2L to 0L,
        2L to 1L,
        2L to 2L
    )
    val r4 = mutableSetOf(
        0L to 0L,
        0L to 1L,
        0L to 2L,
        0L to 3L
    )
    val r5 = mutableSetOf(
        0L to 0L,
        1L to 0L,
        0L to 1L,
        1L to 1L
    )
    return mutableListOf(
        Rock(r1, 4, 1),
        Rock(r2, 3, 3),
        Rock(r3, 3, 3),
        Rock(r4, 1, 4),
        Rock(r5, 2, 2)
    )
}

/**
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
 */