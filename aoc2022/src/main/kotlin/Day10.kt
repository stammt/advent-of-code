import java.io.File
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day10input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day10sample.txt").readLines()
//    val input = listOf(
//        "noop",
//        "addx 3",
//        "addx -5"
//    )

    day10part2(input)
}

fun tick(cycle: Int, value: Int) : Int {
//    println("Cycle $cycle value: $value")
    if ((cycle - 20) % 40 == 0) {
        val signalStrength = cycle * value
        println("cycle $cycle ($value) signalStrength: $signalStrength")
        return signalStrength
    }
    return 0
}

fun day10part1(input: List<String>) {
    var cycle = 0
    var reg = 1
    var result = 0

    for (line in input) {
        cycle++
        result += tick(cycle, reg)
        val op = line.split(" ")[0]
        if (op == "addx") {
            val value = line.split(" ")[1].toInt()
            cycle++
            result += tick(cycle, reg)
            reg += value
        }
    }
    println("After last cycle $cycle reg is $reg")

    println("Result: $result")
}

//fun draw(cycle: Int, reg: Int, result: MutableList<String>) {
//    val lineIndex = (cycle-1) / 40
//    if (lineIndex >= result.size) result.add("")
//    val line = result[lineIndex]
//    val pos = (cycle-1) % 40
//    val sprite = IntRange(reg - 1, reg + 1)
//    val pixel = if (sprite.contains(pos)) '#' else '.'
////    println("Cycle $cycle pos $pos reg $reg line $lineIndex sprite $sprite adding $pixel")
//    result[lineIndex] = (line + pixel)
//}

fun draw(cycle: Int, reg: Int, result: MutableList<Char>) {
    val lineIndex = (cycle-1) / 40
    val sprite = IntRange(reg + (lineIndex * 40) - 1, reg + (lineIndex * 40) + 1)
    val pixel = if (sprite.contains(cycle-1)) '#' else '.'
    result.add(pixel)
}

fun day10part2(input: List<String>) {
    var cycle = 0
    var reg = 1
    var result = mutableListOf<Char>()

    for (line in input) {
        cycle++
        draw(cycle, reg, result)
        val op = line.split(" ")[0]
        if (op == "addx") {
            val value = line.split(" ")[1].toInt()
            cycle++
            draw(cycle, reg, result)
            reg += value
        }
    }

    for (i in result.indices) {
        if (i %40 == 0) println()
        print(result[i])
    }
}
