import java.io.File
import java.lang.Math.floor
import java.time.Duration
import java.time.Instant
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day8input.txt").readLines()

//    val input = listOf<String>("nop +0",
//            "acc +1",
//            "jmp +4",
//            "acc +3",
//            "jmp -3",
//            "acc -99",
//            "acc +1",
//            "jmp -4",
//            "acc +6")
    day8Part2(input)
}

fun day8Part2(input : List<String>) {
    var acc = 0
    val changedPositions = mutableSetOf<Int>()

    while (true) {

        val executedLines = mutableSetOf<Int>()
        acc = 0
        var pos = 0
        var swapped = false
        var looped = false

        while (true) {
            if (executedLines.contains(pos)) {
                println("already executed $pos")
                looped = true
                break
            }
            if (pos == input.size) {
                println("finished execution!")
                break
            }
            executedLines.add(pos)

            var cmd = input[pos].substring(0, 3)
            val value = input[pos].substring(4).toInt()
            if (!swapped && !changedPositions.contains(pos) && (cmd == "jmp" || cmd == "nop")) {
                println("swapping line $pos")
                swapped = true
                changedPositions.add(pos)
                cmd = when(cmd) { "jmp" -> "nop"; "nop" -> "jmp"; else -> {println("?? swap from $cmd"); cmd;}}
            }
            when (cmd) {
                "acc" -> {
                    acc += value; pos++; }
                "jmp" -> pos += value
                "nop" -> pos++
                else -> "what is $cmd"
            }
        }

        if (!looped) {
            break
        }
    }

    println("acc $acc")
}


fun day8Part1(input : List<String>) {
    val executedLines = mutableSetOf<Int>()
    var acc = 0
    var pos = 0

    while (true) {
        if (executedLines.contains(pos)) {
            println("already executed $pos")
            break
        }
        executedLines.add(pos)

        val me = pos
        val cmd = input[pos].substring(0, 3)
        val value = input[pos].substring(4).toInt()
        println("$cmd $value")
        when (cmd) {
            "acc" -> { acc += value; pos++; }
            "jmp" -> pos += value
            "nop" -> pos++
            else -> "what is $cmd"
        }
        println("Executed $me : acc=${acc} pos=${pos}")
    }

    println("acc $acc")
}

