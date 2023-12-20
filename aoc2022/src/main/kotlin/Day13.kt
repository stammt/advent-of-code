import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day13input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day13sample.txt").readLines()
    day13part2(input)
}

interface PacketValue : Comparable<PacketValue> {
//    fun compareTo(other: PacketValue) : Int
}

data class IntValue(val value: Int) : PacketValue {
    override fun compareTo(other: PacketValue): Int {
        return if (other is IntValue) {
            if (value == other.value) 0 else if (value < other.value) -1 else 1
        } else {
            ListValue(mutableListOf(this)).compareTo(other)
        }
    }

    override fun equals(other: Any?): Boolean {
        return if (other is IntValue) {
            value == other.value
        } else {
            false
        }
    }
}

data class ListValue(private val values: List<PacketValue>) : PacketValue {
    override fun compareTo(other: PacketValue): Int {
        if (other is IntValue) {
            return compareTo(ListValue(listOf(other)))
        } else {
            val otherList = other as ListValue
            var i = 0
            while (i < values.size) {
                if (i >= otherList.values.size) {
                    // Right ran out of values first
                    return 1
                } else {
                    val left = values[i]
                    val right = otherList.values[i]
                    val comp = left.compareTo(right)
                    if (comp != 0) return comp
                }
                i++
            }
            return if (i < otherList.values.size) {
                // left ran out of values
                -1
            } else {
                0
            }
        }
    }

    override fun equals(other: Any?): Boolean {
        return if (other is ListValue) {
            values == other.values
        } else {
            false
        }
    }
}

fun parsePacket(line: String) : PacketValue {
    var i = 1 // skip first open bracket

    val values = mutableListOf<PacketValue>()
    while (i < line.length) {
        if (line[i] == ']') {
            // end
            break
        } else if (line[i] == '[') {
            // start a sublist - consume until matching end bracket
            var level = 1
            val start = i
            i++
            do {
               if (line[i] == '[') level++
               else if (line[i] == ']') level--
               i++
            } while (level > 0)
//            println("Parsing sublist ${line.substring(start, i)}")
            values.add(parsePacket(line.substring(start, i)))
            // consume the next comma if there is one
            if (line[i] == ',') {
                i++
            }
        } else if (line[i].isDigit()) {
            // consume the number
            var numberString = ""
            while (line[i].isDigit()) {
                numberString += line[i]
                i++
            }
            values.add(IntValue(numberString.toInt()))
            // consume the next comma if there is one
            if (line[i] == ',') {
                i++
            }
        } else {
            println("Skipping char ${line[i]}")
            i++
        }
    }
    return ListValue(values)
}

fun day13part2(input: List<String>) {
    val separator1 = ListValue(listOf(ListValue(listOf(IntValue(2)))))
    val separator2 = ListValue(listOf(ListValue(listOf(IntValue(6)))))

    val packets = mutableListOf<PacketValue>()
    packets.add(separator1)
    packets.add(separator2)

    for (line in input) {
        if (line.isNotEmpty()) {
            packets.add(parsePacket(line))
        }
    }

    packets.sort()
    val i1 = packets.indexOf(separator1) + 1
    val i2 = packets.indexOf(separator2) + 1
    println("$i1 * $i2 = ${i1 * i2}")
}


fun day13part1(input: List<String>) {
    var i = 0
    var pair = 1
    var sum = 0
    while (i < input.size - 1) {
        val left = parsePacket(input[i++])
        val right = parsePacket(input[i++])
        i++

        val result = left.compareTo(right)
        println("pair $pair result $result")
        if (result == -1) {
            sum += pair
        }
        pair++
    }

    println("sum $sum")
}
