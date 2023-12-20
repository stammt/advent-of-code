import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day06input.txt").readLines()
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
    day06part1(input[0])
}



fun day06part2(input: List<String>) {
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

fun day06part1(input: String) {

    var result = -1
    for (i in 13 until input.length) {
        val candidate = input.subSequence(i-13, i+1)
//        println("testing $candidate at $i")
        if (candidate.toHashSet().size == 14) {
            result = i+1
            break
        }
    }
    println("result: $result")
}

