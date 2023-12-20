import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day01input.txt").readLines()

    val elves = mutableListOf<Int>()
    var current = 0
    for (c in input) {
        if (c.isEmpty()) {
            elves.add(current)
            current = 0
        } else {
            current += c.toInt()
        }
    }

    val max = elves.max()
    println("found ${elves.size} elves, max is $max")

    val top3 = elves.sortedDescending().take(3).sum()
    println("sum $top3")

}

fun part1(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2021aoc/day01input.txt").readLines().map{it.toInt()}
    var increased = 0
    var last = -1

    input.forEach { i ->
        if (last != -1) {
            if (i > last) {
                increased++
            }
        }
        last = i
    }

    println("Increased $increased out of ${input.size}")

}