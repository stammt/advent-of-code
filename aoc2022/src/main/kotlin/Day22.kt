import java.io.File
import java.lang.IllegalArgumentException
import java.lang.IllegalStateException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
//    val input = File("/Users/stammt/Documents/2022aoc/day22input.txt").readLines()
    val input = File("/Users/stammt/Documents/2022aoc/day22sample.txt").readLines()
    day22part2(input)
}

enum class Face {
    FRONT, BACK, TOP, BOTTOM, LEFT, RIGHT
}

fun day22part2(input: List<String>) {
    val board = mutableMapOf<Pair<Int, Int>, Char>()
    val turns = mutableListOf<String>()
    var i = 0
    while (input[i].isNotBlank()) {
        for (x in input[i].indices) {
            if (input[i][x] == '.' || input[i][x] == '#') {
                board[x to i] = input[i][x]
            }
        }
        i++
    }
    i++
    var x = 0
    var turn = ""
    while (x < input[i].length) {
        if (input[i][x].isDigit()) {
            turn += input[i][x]
        } else {
            turns.add(turn)
            turn = ""
            turns.add("" + input[i][x])
        }
        x++
    }
    turns.add(turn)

//    println("Board: $board")
//    println("Turns: $turns")

    // Split the board into 6 sides of 50x50 each, then define a transform between them
    // that tells how to turn the "facing" and how to map between edges. I guess
    // we'll just hardcode which face is which.

    // For sample board, 4x4 faces:
    val top = board.filter { it.key.second < 4 } // 1
    val back = board.filter { it.key.second in 4..7 && it.key.first < 4 } // 2
    val left = board.filter { it.key.second in 4..7 && it.key.first in 4..7 } // 3
    val front = board.filter { it.key.second in 4..7 && it.key.first > 7 } // 4
    val bottom = board.filter { it.key.second > 7 && it.key.first in 8..11 } // 5
    val right = board.filter { it.key.second > 7 && it.key.first > 11 } // 6

    val faceOrigins = mutableMapOf<Face, Pair<Int, Int>>(
        Face.TOP to (8 to 0),
        Face.RIGHT to (12 to 8),
        Face.BOTTOM to (8 to 8),
        Face.LEFT to (4 to 4),
        Face.FRONT to (8 to 4),
        Face.BACK to (0 to 4)
    )


    val cube = SampleCubeDefinition()

    val minX = board.filter{ it.key.second == 0 && board[it.key] == '.'  }.map { it.key.first }.min()

    var facing = 0
    var pos = minX to 0
    var face = Face.TOP
    println("Starting at $pos")
    for (turn in turns) {
        if (turn[0].isDigit()) {
            pos = move(turn.toInt(), pos, facing, board)
        } else {
            facing = turn(turn, facing)
        }
    }

    var result = (1000 * (pos.second + 1)) + (4 * (pos.first + 1)) + facing
    println("Result $result ($pos facing $facing)")
}


fun day22part1(input: List<String>) {
    val board = mutableMapOf<Pair<Int, Int>, Char>()
    val turns = mutableListOf<String>()
    var i = 0
    while (input[i].isNotBlank()) {
        for (x in input[i].indices) {
            if (input[i][x] == '.' || input[i][x] == '#') {
                board[x to i] = input[i][x]
            }
        }
        i++
    }
    i++
    var x = 0
    var turn = ""
    while (x < input[i].length) {
        if (input[i][x].isDigit()) {
            turn += input[i][x]
        } else {
            turns.add(turn)
            turn = ""
            turns.add("" + input[i][x])
        }
        x++
    }
    turns.add(turn)

    println("Board: $board")
    println("Turns: $turns")

    val minX = board.filter{ it.key.second == 0 && board[it.key] == '.'  }.map { it.key.first }.min()

    var facing = 0
    var pos = minX to 0
    println("Starting at $pos")
    for (turn in turns) {
        if (turn[0].isDigit()) {
            pos = move(turn.toInt(), pos, facing, board)
        } else {
            facing = turn(turn, facing)
        }
    }

    var result = (1000 * (pos.second + 1)) + (4 * (pos.first + 1)) + facing
    println("Result $result ($pos facing $facing)")
}

class SampleCubeDefinition() {
    fun getNextFace(pos: Pair<Int, Int>, face: Face, facing: Int) : FaceTransition {
        if (face == Face.TOP) {
            val nextFacing = when (facing) {
                0 -> 3
                1 -> 1
                2 -> 1
                3 -> 1
                else -> throw IllegalArgumentException()
            }
            val nextFace = when (facing) {
                0 -> Face.RIGHT
                1 -> Face.FRONT
                2 -> Face.LEFT
                3 -> Face.BACK
                else -> throw IllegalArgumentException()
            }
            val nextPos = when (facing) {
                0 -> 3 to 3 - pos.second
                1 -> pos.first to 0
                2 -> pos.second to 0
                3 -> 0 to 3 - pos.second
                else -> throw IllegalArgumentException()
            }
            return FaceTransition(nextFacing, nextFace, nextPos)
        } else if (face == Face.RIGHT) {
            val nextFacing = when (facing) {
                0 -> 2
                1 -> 0
                2 -> 2
                3 -> 1
                else -> throw IllegalArgumentException()
            }
            val nextFace = when (facing) {
                0 -> Face.FRONT
                1 -> Face.BOTTOM
                2 -> Face.BACK
                3 -> Face.TOP
                else -> throw IllegalArgumentException()
            }
            val nextPos = when (facing) {
                0 -> 0 to pos.second
                1 -> 0 to 3 - pos.first
                2 -> 3 to pos.second
                3 -> 0 to pos.first
                else -> throw IllegalArgumentException()
            }
            return FaceTransition(nextFacing, nextFace, nextPos)
        } else if (face == Face.BOTTOM) {
            val nextFacing = when (facing) {
                0 -> 0
                1 -> 1
                2 -> 3
                3 -> 3
                else -> throw IllegalArgumentException()
            }
            val nextFace = when (facing) {
                0 -> Face.RIGHT
                1 -> Face.BACK
                2 -> Face.LEFT
                3 -> Face.FRONT
                else -> throw IllegalArgumentException()
            }
            val nextPos = when (facing) {
                0 -> 0 to pos.second
                1 -> pos.first to 0
                2 -> 3 - pos.second to 3
                3 -> pos.first to 3
                else -> throw IllegalArgumentException()
            }
            return FaceTransition(nextFacing, nextFace, nextPos)
        } else if (face == Face.LEFT) {
            val nextFacing = when (facing) {
                0 -> 0
                1 -> 1
                2 -> 2
                3 -> 1
                else -> throw IllegalArgumentException()
            }
            val nextFace = when (facing) {
                0 -> Face.FRONT
                1 -> Face.BOTTOM
                2 -> Face.BACK
                3 -> Face.TOP
                else -> throw IllegalArgumentException()
            }
            val nextPos = when (facing) {
                0 -> 0 to pos.second
                1 -> 0 to 3 - pos.first
                2 -> 3 to pos.second
                3 -> 0 to pos.first
                else -> throw IllegalArgumentException()
            }
            return FaceTransition(nextFacing, nextFace, nextPos)
        } else if (face == Face.FRONT) {
            val nextFacing = when (facing) {
                0 -> 1
                1 -> 1
                2 -> 2
                3 -> 3
                else -> throw IllegalArgumentException()
            }
            val nextFace = when (facing) {
                0 -> Face.RIGHT
                1 -> Face.BOTTOM
                2 -> Face.LEFT
                3 -> Face.TOP
                else -> throw IllegalArgumentException()
            }
            val nextPos = when (facing) {
                0 -> 0 to 0 - pos.second
                1 -> pos.first to 0
                2 -> 3 to pos.second
                3 -> pos.first to 3
                else -> throw IllegalArgumentException()
            }
            return FaceTransition(nextFacing, nextFace, nextPos)
        } else if (face == Face.BACK) {
            val nextFacing = when (facing) {
                0 -> 0
                1 -> 3
                2 -> 3
                3 -> 1
                else -> throw IllegalArgumentException()
            }
            val nextFace = when (facing) {
                0 -> Face.LEFT
                1 -> Face.BOTTOM
                2 -> Face.RIGHT
                3 -> Face.TOP
                else -> throw IllegalArgumentException()
            }
            val nextPos = when (facing) {
                0 -> 0 to pos.second
                1 -> 3-pos.first to 3
                2 -> 3-pos.first to 3
                3 -> 0 to 3-pos.first
                else -> throw IllegalArgumentException()
            }
            return FaceTransition(nextFacing, nextFace, nextPos)
        } else {
            throw IllegalStateException()
        }
    }
}

data class FaceTransition(val nextFacing: Int, val nextFace: Face, val nextPos: Pair<Int, Int>)

fun turn(dir: String, facing: Int) : Int {
    val next = if (dir == "R") facing + 1 else facing - 1
    return if (next > 3) 0 else if (next < 0) 3 else next
}

fun move(count: Int, pos: Pair<Int, Int>, facing: Int, board: Map<Pair<Int, Int>, Char>) : Pair<Int, Int> {
    var nextPos = pos
    for (i in 0 until count) {
        val maxX = board.filter{it.key.second == nextPos.second  }.map { it.key.first }.max()
        val minX = board.filter{it.key.second == nextPos.second }.map { it.key.first }.min()
        val maxY = board.filter{it.key.first == nextPos.first }.map { it.key.second }.max()
        val minY = board.filter{it.key.first == nextPos.first }.map { it.key.second }.min()
        println("For $nextPos $minX $minY and $maxX $maxY")
        var nextX = nextPos.first
        var nextY = nextPos.second
        if (facing == 0) {
            nextX++
            if (nextX > maxX) {
                nextX = minX
            }
        } else if (facing == 2) {
            nextX--
            if (nextX < minX) {
                nextX = maxX
            }
        } else if (facing == 1) {
            nextY++
            if (nextY > maxY) {
                nextY = minY
            }
        } else if (facing == 3) {
            nextY--
            if (nextY < minY) {
                nextY = maxY
            }
        } else {
            throw IllegalArgumentException("Unknown facing $facing")
        }

        if (board[nextX to nextY] == '#') {
            println("Would hit a wall")
            break
        } else {
            println("Stepping to $nextX,$nextY")
            nextPos = nextX to nextY
        }
    }
    println("Moved from $pos to $nextPos facing $facing")
    return nextPos
}


