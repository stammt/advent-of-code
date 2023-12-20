import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day22input.txt").readLines()

//    val input = ("Player 1:\n" +
//            "9\n" +
//            "2\n" +
//            "6\n" +
//            "3\n" +
//            "1\n" +
//            "\n" +
//            "Player 2:\n" +
//            "5\n" +
//            "8\n" +
//            "4\n" +
//            "7\n" +
//            "10").split("\n")

    var p1 = mutableListOf<Int>()
    var p2 = mutableListOf<Int>()

    val p2Start = input.indexOf("Player 2:")
    for (line in input.subList(1, p2Start).map { it.trim() }) {
        if (line.isNotEmpty()) {
            p1.add(line.toInt())
        }
    }
    for (line in input.subList(p2Start + 1, input.size).map { it.trim() }) {
        if (line.isNotEmpty()) {
            p2.add(line.toInt())
        }
    }

    println("${p1.size} - ${p2.size}")

    day22Part2(p1, p2)
}

fun day22Part2(p1: MutableList<Int>, p2: MutableList<Int>) {
    val c = combat(p1, p2, mutableListOf(), mutableListOf())
    //val winner = when (p1.isNotEmpty()) {true -> p1; false -> p2; }
    val winner = if (p1.isNotEmpty()) p1 else p2

    val result = winner.foldIndexed(0) { index, acc, i -> acc + (i * (winner.size - index))}
    println("result: $result")
}

fun combat(p1: MutableList<Int>, p2: MutableList<Int>, p1History: MutableList<List<Int>>, p2History: MutableList<List<Int>>) : Int {
    println("starting combat with ($p1) vs ($p2)")

    while (p1.isNotEmpty() && p2.isNotEmpty()) {
        if (p1History.contains(p1) && p2History.contains(p2)) {
            println("bailing, we've been here before $p1 $p2")
            return 0
        }

        p1History.add(p1.toList())
        p2History.add(p2.toList())

        val p1Card = p1.removeAt(0)
        val p2Card = p2.removeAt(0)

        val winner = if (p1.size >= p1Card && p2.size >= p2Card) {
            val subP1 = p1.subList(0, p1Card).toMutableList()
            val subP2 = p2.subList(0, p2Card).toMutableList()

            combat(subP1, subP2, mutableListOf(), mutableListOf())
        } else {
            when (p1Card > p2Card) { true-> 0; false -> 1; }
        }

        when (winner) {
            0 -> {
                p1.add(p1Card)
                p1.add(p2Card)
            }
            1 -> {
                p2.add(p2Card)
                p2.add(p1Card)
            }
        }
    }

    return when (p1.isNotEmpty()) {true->0; false -> 1;}
}

fun day22Part1(p1: MutableList<Int>, p2: MutableList<Int>) {

    while (p1.isNotEmpty() && p2.isNotEmpty()) {
        val p1Card = p1.removeAt(0)
        val p2Card = p2.removeAt(0)
        if (p1Card > p2Card) {
            p1.add(p1Card)
            p1.add(p2Card)
        } else {
            p2.add(p2Card)
            p2.add(p1Card)
        }
    }

    val winner = when (p1.isNotEmpty()) {true->p1; false -> p2; }
    println("winner $winner")
    val size = winner.size
    var result = 0
    for (i in 0 until size) {
        result += (winner[i] * (size - i))
    }

    // 33756 too high
    println("result: $result")

}

