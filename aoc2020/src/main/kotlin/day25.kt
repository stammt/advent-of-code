import java.awt.Point
import java.io.File

fun main(args: Array<String>) {
    val input = ("11239946\n" +
            "10464955").split("\n")
    val sampleInput = ("5764801\n" +
            "17807724").split("\n")

    day25Part1(input.map{ it.toLong() })
}

fun day25Part1(input: List<Long>) {

    var loopSize1 = -1
    var loopSize2 = -1
    val values = mutableListOf<Long>()
    val subjectNumber = 7L
    var v = 1L
    var loopSize = 0
    while (loopSize1 == -1 || loopSize2 == -1) {
        loopSize++
        v = loop(v, subjectNumber)
        values.add(v)
        if (v == input[0]) {
            loopSize1 = loopSize
        } else if (v == input[1]) {
            loopSize2 = loopSize
        }
        if (loopSize1 != -1 && loopSize2 != -1) break
    }
    println("loopSize1 = $loopSize1 ; loopSize2 = $loopSize2")

    if (loopSize1 > -1) {
        var key1 = 1L
        for (i in 1..loopSize1) {
            key1 = loop(key1, input[1])
        }
        println("result1 $key1")
    }
    if (loopSize2 > -1) {
        var key2 = 1L
        for (i in 1..loopSize2) {
            key2 = loop(key2, input[0])
        }

        println("result2 $key2")
    }
}

fun loop(value: Long, subject: Long) : Long {
    return (value * subject) % 20201227L
}

