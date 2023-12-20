import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day04input.txt").readLines()
//    val input = listOf(
//        "2-4,6-8",
//        "2-3,4-5",
//        "5-7,7-9",
//        "2-8,3-7",
//        "6-6,4-6",
//        "2-6,4-8"    )

    day04part2(input)
}

fun day04part2(input: List<String>) {
    var total = 0
    for (line in input) {
        var ranges = line.split(',').map { it.split("-") }
            .map { IntRange(it[0].toInt(), it[1].toInt()) }

        if (ranges[0].intersect(ranges[1]).isNotEmpty()) {
            total++
        }
    }

    println("total: $total")
}

fun contains(a: IntRange, b: IntRange) : Boolean {
    return (a.first <= b.first && a.last >= b.last)
}

fun day04part1(input: List<String>) {
    var total = 0
    for (line in input) {
        var ranges = line.split(',').map { it.split("-") }
            .map { IntRange(it[0].toInt(), it[1].toInt()) }

        if (contains(ranges[0], ranges[1]) || contains(ranges[1], ranges[0])) {
            total++
        }
    }

    println("total: $total")
}

