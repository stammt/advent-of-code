import java.io.File
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day09input.txt").readLines()
//    val input = listOf(
//        "R 4",
//        "U 4",
//        "L 3",
//        "D 1",
//        "R 4",
//        "D 1",
//        "L 5",
//        "R 2"
//    )
//    val input = listOf(
//        "R 5",
//        "U 8",
//        "L 8",
//        "D 3",
//        "R 17",
//        "D 10",
//        "L 25",
//        "U 20"
//    )

    day09part2(input)
}

fun isTouching(head: Pair<Int, Int>, tail: Pair<Int, Int>) : Boolean {
    return abs(head.first - tail.first) <= 1 &&
        abs(head.second - tail.second) <= 1
}

fun move(head: Pair<Int, Int>, direction: String) : Pair<Int, Int> {
    var x = head.first
    var y = head.second

    if (direction == "U") {
        y -= 1
    } else if (direction == "D") {
        y += 1
    } else if (direction == "L") {
        x -= 1
    } else if (direction == "R") {
        x += 1
    }
    return x to y
}

fun chase(head: Pair<Int, Int>, tail: Pair<Int, Int>) : Pair<Int, Int> {
    val x = if (head.first < tail.first) tail.first - 1 else if (head.first > tail.first) tail.first + 1 else tail.first
    val y = if (head.second < tail.second) tail.second - 1 else if (head.second > tail.second) tail.second + 1 else tail.second
    return x to y
}

fun day09part1(input: List<String>) {
    val visited = mutableSetOf<Pair<Int, Int>>()

    val start = 0 to 0
    var head = 0 to 0
    var tail = 0 to 0

    visited.add(start)

    for (line in input) {
        val direction = line.split(" ")[0]
        val count = line.split(" ")[1].toInt()

        for (step in 0 until count) {
            head = move(head, direction)
            if (!isTouching(head, tail)) {
                tail = chase(head, tail)
                visited.add(tail)
            }
        }
    }

    println("Result: ${visited.size}")
}

fun day09part2(input: List<String>) {
    val visited = mutableSetOf<Pair<Int, Int>>()

    val start = 0 to 0
    val knots = mutableListOf<Pair<Int, Int>>()
    for (i in 1..10) {
        knots.add(Pair(0, 0))
    }
    visited.add(start)

    for (line in input) {
        val direction = line.split(" ")[0]
        val count = line.split(" ")[1].toInt()

        for (step in 0 until count) {
            knots[0] = move(knots[0], direction)
            for (i in 1 until knots.size) {
                if (!isTouching(knots[i], knots[i-1])) {
                    knots[i] = chase(knots[i-1], knots[i])
                    if (i == knots.size - 1) {
                        visited.add(knots[i])
                    }
                }
            }
        }
    }

    println("Result: ${visited.size}")
}
