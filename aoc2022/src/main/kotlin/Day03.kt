import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day03input.txt").readLines()
//    val input = listOf(
//        "vJrwpWtwJgWrhcsFMMfFFhFp",
//                "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
//                "PmmdzqPrVvPwwTWBwg",
//                "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
//                "ttgJtRGJQctTZtZT",
//                "CrZsJsPPZsGzwwsLwLmpwMDw"
//    )

    day03part2(input)
}

fun day03part2(input: List<String>) {
    var total = 0
    var elfCount = input.size / 3
    var badge: Char? = null
    for (g in 0 until elfCount) {
        var start = g * 3
        for (c in input[start]) {
            if (input[start+1].contains(c) && input[start+2].contains(c)) {
                badge = c
                break
            }
        }

        if (badge != null) {
            var priority = 0
            if (badge.isLowerCase()) {
                priority = badge - 'a' + 1
            } else {
                priority = badge - 'A' + 27
            }
            total += priority
        }
    }

    println("total: $total")
}


fun day03part1(input: List<String>) {
    var total = 0
    for (line in input) {
        var i1 = line.take(line.length / 2)
        var i2 = line.takeLast(line.length / 2)
        var item: Char? = null
        for (i in i1) {
            if (i2.contains(i)) {
                item = i
                break
            }
        }

        if (item != null) {
            var priority = 0
            if (item.isLowerCase()) {
                priority = item - 'a' + 1
            } else {
                priority = item - 'A' + 27
            }
            total += priority
        }
    }

    println("total: $total")
}

