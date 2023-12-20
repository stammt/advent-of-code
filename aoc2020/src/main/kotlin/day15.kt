import java.io.File
import java.lang.Math.floor
import java.time.Duration
import java.time.Instant
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day14input.txt").readLines()

//    val input = listOf<String>("mask = 000000000000000000000000000000X1001X",
//            "mem[42] = 100",
//            "mask = 00000000000000000000000000000000X0XX",
//            "mem[26] = 1")

//    val input = listOf<String>("mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
//            "mem[8] = 11",
//            "mem[7] = 101",
//            "mem[8] = 0")
    day15Part1(listOf(2,1,10,11,0,6))
//    day15Part1(listOf(0,3,6))
}

fun day15Part1(input: List<Int>) {
    val numbers = mutableListOf<Int>()
    val lastNumber = mutableMapOf<Int, Int>()

    numbers.addAll(input)
    numbers.forEachIndexed{i, number -> lastNumber[number] = i }

    val stop = 30000000
    for (i in (input.size - 1) until stop) {
        val lastSpoken = numbers[i]
        val previousIndex = lastNumber[lastSpoken] ?: -1
        val nextNumber = when (previousIndex) {
            -1 -> 0
            else -> (i - previousIndex)
        }
        lastNumber[lastSpoken] = i
        numbers.add(nextNumber)
    }

    print("result ${numbers[stop - 1]}")
}

