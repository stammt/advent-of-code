import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day02input.txt").readLines()
//    val input = listOf("A Y", "B X", "C Z")

    val state = mutableListOf<List<Int>>()
    state.add(mutableListOf(3, 0, 6))
    state.add(mutableListOf(6, 3, 0))
    state.add(mutableListOf(0, 6, 3))

    day02part2(input, state)
}

fun day02part2(input: List<String>, state: List<List<Int>>) {
    var total = 0
    for (line in input) {
        var shapes = line.split(" ")
        var elf = shapes[0].first() - 'A'
        var neededState = (shapes[1].first() - 'X') * 3
        var me = state.indexOfFirst { row -> row[elf] == neededState }

        println("elf $elf need $neededState me $me")
        var result = state[me][elf]
        var score = result + (me + 1)
        println("result: $result score: $score")
        total += score
    }

    println("total: $total")
}


fun day02part1(input: List<String>, state: List<List<Int>>) {
    var total = 0
    for (line in input) {
        var shapes = line.split(" ")
        var elf = shapes[0].first() - 'A'
        var me = shapes[1].first() - 'X'
        println("elf $elf me $me")
        var result = state[me][elf]
        var score = result + (me + 1)
        println("result: $result score: $score")
        total += score
    }

    println("total: $total")
}

