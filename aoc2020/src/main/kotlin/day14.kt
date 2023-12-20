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
    day14Part2(input)
}

fun day14Part2(input: List<String>) {
    val mem = mutableMapOf<Long, Long>()
    var mask = ""
    input.forEach {
        val segments = it.split(" = ")
        if (segments[0] == "mask") {
            mask = segments[1]
            println("new mask $mask")
        } else if (segments[0].startsWith("mem[")) {
            val segmentId = segments[0].substring("mem[".length, segments[0].length - 1).toInt()
            val segmentBinaryString = Integer.toBinaryString(segmentId).padStart(36, '0')
            println("writing to address $segmentBinaryString ($segmentId)")

            var xIndices = mutableListOf<Int>()
            mask.forEachIndexed{ index, c ->
                if (c == 'X') {
                    xIndices.add(index)
                }
            }

            var oneIndices = mutableListOf<Int>()
            mask.forEachIndexed{ index, c ->
                if (c == '1') {
                    oneIndices.add(index)
                }
            }

            // build a list of all combinations of 1's and 0's by making a list of
            // 0..2^(number of X characters in the mask), as binary
            val combos = Math.pow(2.0, xIndices.size.toDouble()).toInt()
            val bins = mutableListOf<String>()
            for (i in 0 until combos) {
                bins.add(Integer.toBinaryString(i). padStart(xIndices.size, '0'))
            }

            // for each combination, replace the X's with the characters in the binary
            // number at that index.
            val decimalValue = segments[1].toLong()
            bins.forEach{ subst ->
                var updatedSegmentBinaryString = segmentBinaryString.toCharArray()
                xIndices.forEachIndexed { indexIndex, i ->
                    updatedSegmentBinaryString[i] = subst[indexIndex]
                }
                oneIndices.forEachIndexed { indexIndex, i ->
                    updatedSegmentBinaryString[i] = '1'
                }

                println("writing $decimalValue to ${updatedSegmentBinaryString.joinToString("")}")

                val memLocation = updatedSegmentBinaryString.joinToString("").toLong(2)
                mem[memLocation] = decimalValue
            }
        }
    }

    var sum = 0L
    mem.forEach{
        sum += it.value
    }

    println("sum: $sum")
}

fun day14Part1(input : List<String>) {
    val mem = mutableMapOf<Int, Long>()
    var mask = ""
    input.forEach{
        val segments = it.split(" = ")
        if (segments[0] == "mask") {
            mask = segments[1]
            println("new mask $mask")
        } else if (segments[0].startsWith("mem[")) {
            val segmentId = segments[0].substring("mem[".length, segments[0].length - 1).toInt()
            val decimalValue = segments[1].toInt()
            val binaryString = Integer.toBinaryString(decimalValue).padStart(36, '0')

            var updatedString = ""
            binaryString.forEachIndexed{index, ch ->
                if (mask[index] == 'X') {
                    updatedString += ch
                } else {
                    updatedString += mask[index]
                }
            }
            mem[segmentId] = updatedString.toLong(2)
            println("storing $decimalValue ($binaryString) -- now ${mem[segmentId]} ($updatedString) in $segmentId")
        } else {
            println("unknown line $it")
        }
    }

    var sum = 0L
    mem.forEach{
        sum += it.value
    }

    println("sum: $sum")

}

