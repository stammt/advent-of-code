import java.io.File
import java.lang.IllegalArgumentException
import java.lang.IllegalStateException
import java.lang.Math.pow
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min
import kotlin.math.pow

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day25input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day25sample.txt").readLines()
    day25part1(input)
}

fun day25part1(input: List<String>) {
    var sum = 0.0

    for (line in input) {
        var lineTotal = 0.0
//        println("Parsing line $line")
        for (i in line.indices.reversed()) {
            val d = line[i]
            val place = 5.0.pow((line.length - 1) - i)
            if (d.isDigit()) {
//                println("+ ${(place * d.toString().toInt())} (from $d $place at $i)")
                lineTotal += (place * d.toString().toInt())
            } else if (d == '-') {
//                println("- $place")
                lineTotal -= place
            } else if (d == '=') {
//                println("- 2*$place")
                lineTotal -= (2*place)
            }
        }
        println("$lineTotal == $line")
        sum += lineTotal
    }

    println("Sum: $sum")

    var x = sum.toLong()
    var i = 0
    var snafu = ""

    // find the number of digits by going until 2*place - 2*(place-1) would be too large
    var len = 0
    var prev = 0.0
    do {
        val v = 2*(5.0.pow(len))
        println("len $len v $v")
        if (v - prev > x) {
            println("v $v prev $prev x $x")
            break
        }
        prev += v
        len++
    } while (true)

    println("Snafu is $len digits")
    var rem = x.toDouble()
    for (d in 0 until len) {
        val place = 5.0.pow(d)
        val nextPlace = 5.0.pow(d + 1)

        val remainder = rem % nextPlace
        if (remainder <= (2 * place)) {
            snafu = (remainder / place).toInt().toString() + snafu
            rem -= remainder
        } else if (nextPlace == remainder + (2 * place)) {
            snafu = "=" + snafu
            rem += 2.0 * place
        } else if (nextPlace == (remainder + place)) {
            snafu = "-" + snafu
            rem += place
        } else {
            println("Don't know what to do with remainder $remainder")
        }

//        println("D $d snafu now $snafu remainder was $remainder new value $rem at place $place nextPlace $nextPlace")
    }

    println("Snafu: $snafu")

}

/**
 * 4890 % 5 =   0 -> 0
 * 4890 % 25 = 15 -> = (add 10 to get to 25)
 * 4900 % 125 = 25 -> 1 (subtract 25)
 * 4875 % 625 = 500 -> - (add 125 to get to 625)
 * 5000 % 1250 = 0 -> 0
 * 5000 % 3125 = 1875 -- know we end here because 6250 is higher
 */