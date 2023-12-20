import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day05input.txt").readLines()
//    val input = listOf(
//        "    [D]",
//        "[N] [C]",
//        "[Z] [M] [P]",
//        "1   2   3",
//"",
//                "move 1 from 2 to 1",
//                "move 3 from 1 to 3",
//                "move 2 from 2 to 1",
//                "move 1 from 1 to 2"
//    )

//    parseCrates(input)
    day05part2(input)
}

fun parseCrates(input: List<String>) : List<MutableList<Char>> {
    val crates = input.takeWhile { it.isNotEmpty() }
    val stacks = crates.last().trim().split("\\s+".toRegex()).map { mutableListOf<Char>() }
    for (line in crates.dropLast(1)) {
        var i = 0
        var stack = 0
        while (i < line.length) {
            val crate = line.substring(i, i+3).trim()
            if (crate.isNotEmpty()) {
                val label = crate[1]
                stacks[stack].add(0, label)
            }
            i += 4
            stack++
        }
    }
//    println(stacks)
    return stacks
}


fun day05part2(input: List<String>) {
    val crates = parseCrates(input)
    val ops = input.dropWhile { it.isNotEmpty() }.drop(1)

    println("first: $crates")
    for (op in ops) {
//        println(op)
        val parsed = op.split(" ")
        val count = parsed[1].toInt()
        val fromStack = parsed[3].toInt() - 1
        val toStack = parsed[5].toInt() - 1
        val fromStackSize = crates[fromStack].size
        crates[toStack].addAll(crates[fromStack].subList(fromStackSize-count, fromStackSize))
        for (i in 1..count) {
            crates[fromStack].removeLast()
        }
//        println(crates)
    }

    println("final: $crates")

    var result = ""
    for (crate in crates) {
        if (crate.isNotEmpty()) {
            result += crate.last()
        } else {
            result += ' '
        }
    }
    println("result: $result")
}

fun day05part1(input: List<String>) {
    val crates = parseCrates(input)
    val ops = input.dropWhile { it.isNotEmpty() }.drop(1)

    println("first: $crates")
    for (op in ops) {
//        println(op)
        val parsed = op.split(" ")
        val count = parsed[1].toInt()
        val fromStack = parsed[3].toInt() - 1
        val toStack = parsed[5].toInt() - 1
        for (i in 1..count) {
            crates[toStack].add(crates[fromStack].removeLast())
        }
//        println(crates)
    }

    println("final: $crates")

    var result = ""
    for (crate in crates) {
        if (crate.isNotEmpty()) {
            result += crate.last()
        } else {
            result += ' '
        }
    }
    println("result: $result")
}

