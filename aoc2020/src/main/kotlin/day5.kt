import java.io.File
import kotlin.math.floor

fun main(args: Array<String>) {
    val passes = File("/Users/stammt/dev/aoc/day5input.txt").readLines()
//    val passIds = passes.map(toPassId).toList()

//    val passes = listOf("FBFBBFFRLR", "BFFFBBFRRR")
    val passIds = mutableListOf<Int>()
    passes.forEach {
        val line = it.trim()
        passIds.add(toPassId(line))
    }
    passIds.sort()
    println(passIds)
    val max = passIds.maxOrNull() // 911
    println("max is $max")

    val mine = day5part2(passIds)
    println("mine is $mine")

}

fun day5part2(passIds: List<Int>) : Int {
    val max = passIds.size - 1
    for (i in 1..max) {
        if (passIds[i] - passIds[i-1] == 2) {
            println("found missing id between ${passIds[i]} and ${passIds[i-1]}")
            return passIds[i-1] + 1
        }
    }
    return -1
}

fun toPassId(pass: String) : Int {
    val rowChars = pass.substring(0, 7)
    val colChars = pass.substring(7, 10)

    val row = toRow(rowChars, 0, 127, 'F', 'B')
    val col = toRow(colChars, 0, 7, 'L', 'R')
    val id = (row * 8) + col
//    println("$pass row $row col $col id $id")
    return id
}

fun toRow(rowChars: String, start: Int, end: Int, lowerHalf: Char, upperHalf: Char): Int {
    val midPoint = start + floor((end - start) / 2.0).toInt()
    println("$midPoint of $start - $end")
    return when(rowChars[0]) {
        lowerHalf -> { if (rowChars.length == 1)  start  else toRow(rowChars.substring(1), start, midPoint, lowerHalf, upperHalf)}
        upperHalf -> { if (rowChars.length == 1)  end else toRow(rowChars.substring(1), midPoint+1, end, lowerHalf, upperHalf)}
        else -> -1
    }
}
