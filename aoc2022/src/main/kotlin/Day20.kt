import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day20input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day20sample.txt").readLines()
    day20part2(input)
}

fun day20part2(input: List<String>) {
    // pair of value to original index
    val list = mutableListOf<Pair<Long, Int>>()
    val key = 811589153
    for (i in input.indices) {
        list.add((input[i].toLong() * key) to i)
    }

    println("Read ${list.size} values")
    println(list)

    for (mix in 0 until 10) {
        for (i in input.indices) {
            val index = list.indexOfFirst { it.second == i }
            val pair = list.removeAt(index)
            var moveTo = (index + pair.first) % list.size
            if (moveTo < 0) {
                moveTo = list.size - (abs(moveTo) % list.size)
            }
            //        println("moving from $index to $moveTo")
            list.add(moveTo.toInt(), pair)
            //        println(list)
        }
        println(list)
    }
    val zeroIndex = list.indexOfFirst { it.first == 0L }
    val n1 = list[(zeroIndex + 1000) % list.size].first
    val n2 = list[(zeroIndex + 2000) % list.size].first
    val n3 = list[(zeroIndex + 3000) % list.size].first
    val sum = n1 + n2 + n3
    println("Sum $sum ($n1 + $n2 + $n3")
}


fun day20part1(input: List<String>) {
    // pair of value to original index
    val list = mutableListOf<Pair<Int, Int>>()
    for (i in input.indices) {
        list.add(input[i].toInt() to i)
    }

    println("Read ${list.size} values")
    println(list)

    for (i in input.indices) {
        val index = list.indexOfFirst { it.second == i }
        val pair = list.removeAt(index)
        var moveTo = (index + pair.first) % list.size
        if (moveTo < 0) {
            moveTo = list.size - (abs(moveTo) % list.size)
        }
//        println("moving from $index to $moveTo")
        list.add(moveTo, pair)
//        println(list)
    }

    val zeroIndex = list.indexOfFirst { it.first == 0 }
    val n1 = list[(zeroIndex + 1000) % list.size].first
    val n2 = list[(zeroIndex + 2000) % list.size].first
    val n3 = list[(zeroIndex + 3000) % list.size].first
    val sum = n1 + n2 + n3
    println("Sum $sum ($n1 + $n2 + $n3")
}
