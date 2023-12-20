import java.io.File
import java.lang.Math.floor
import java.time.Duration
import java.time.Instant
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day16input.txt").readLines()

    day16Part2(input)
}

fun day16Part2(input: List<String>) {
    var allValids = mutableSetOf<Int>()
    var validFieldValues = mutableMapOf<String, Set<Int>>()
    var yourTicket = false
    var nearbyTickets = false
    val validTickets = mutableListOf<List<Int>>()
    var yourTicketNumbers: List<Int> = listOf()
    var error = 0
    input.forEach {
        if (it.trim().isNotEmpty()) {
            if (it.startsWith("your ticket")) {
                yourTicket = true
            } else if (it.startsWith("nearby tickets")) {
                nearbyTickets = true
            } else if (!yourTicket && !nearbyTickets) {
                // valid numbers
                val segments = it.trim().split(":")
                val rangeSegment = segments[1].trim()
                val ranges = rangeSegment.split("or")
                val thisField = mutableSetOf<Int>()
                ranges.forEach {
                    val firstAndLast = it.trim().split("-")
                    val range = firstAndLast[0].trim().toInt()..firstAndLast[1].trim().toInt()
                    allValids.addAll(range)
                    thisField.addAll(range)
                }
                validFieldValues[segments[0].trim()] = thisField
            } else if (yourTicket && !nearbyTickets) {
                yourTicketNumbers = it.trim().split(",").map{ it.toInt() }
                validTickets.add(yourTicketNumbers)
            } else if (nearbyTickets) {
                val numbers = it.trim().split(",").map { it.toInt() }
                var valid = true
                numbers.forEach {
                    if (!allValids.contains(it)) {
                        error += it
                        valid = false
                    }
                }
                if (valid) {
                    validTickets.add(numbers)
                } else {
                    println("ignoring invalid ticket")
                }
            }
        }
    }

    println("field count: ${validFieldValues.size}, ${validTickets.size} valid tickets, ${validTickets[0].size} fields per ticket")

    val valuesAtIndex = mutableListOf<MutableSet<Int>>()
    for (i in 0 until (validFieldValues.size)) {
        valuesAtIndex.add(mutableSetOf())
    }
    validTickets.forEach {
        it.forEachIndexed { index, i ->
            val values: MutableSet<Int> = valuesAtIndex[index]
            values.add(i)
            valuesAtIndex[index] = values
        }
    }
    println("values at index size ${valuesAtIndex.size}")
    val fields = mutableListOf<String>()
    for (i in 0 until validFieldValues.size) {
        fields.add("")
    }
    val allFieldNames = mutableSetOf<String>()
    allFieldNames.addAll(validFieldValues.keys)
    val potentialFieldPositions = mutableListOf<MutableList<String>>()

    valuesAtIndex.forEach {
        val valuesAtThisIndex = it
        val potentialFieldsAtThisIndex = mutableListOf<String>()
        validFieldValues.keys.forEach {
            val fieldName = it
            val validValuesForThisField = validFieldValues[fieldName] ?: setOf<Int>()
            if (validValuesForThisField.containsAll(valuesAtThisIndex)) {
                potentialFieldsAtThisIndex.add(fieldName)
            }
        }
        potentialFieldPositions.add(potentialFieldsAtThisIndex)
    }

    while (true) {
        // fields might overlap, find fields with only one potential fit, assign those,
        // then remove that potential fit from other fields
        var fieldIndex = -1
        var fieldName = ""
        potentialFieldPositions.forEachIndexed { index, it ->
            if (fieldIndex == -1 && it.size == 1) {
                fieldIndex = index
                fieldName = it[0]
            }
        }
        if (fieldIndex == -1) {
            println("didn't find anymore, breaking")
            break
        }
        fields[fieldIndex] = fieldName
        println("setting $fieldIndex to $fieldName")

        // remove this potential field name from other indices
        potentialFieldPositions.forEachIndexed { index, it ->
            it.remove(fieldName)
        }
    }


    println("field order (${fields.size}): $fields")
    var result = 1L
    yourTicketNumbers.forEachIndexed { index, i ->
        val fieldName = fields[index]

        if (fieldName.startsWith("departure")) {
            println("$fieldName = $i")
            result *= i
        }
    }

    println("result: $result")
}


fun day16Part1(input: List<String>) {
    var valids = mutableSetOf<Int>()
    var yourTicket = false
    var nearbyTickets = false
    var error = 0
    input.forEach {
        if (it.trim().isNotEmpty()) {
            if (it.startsWith("your ticket")) {
                yourTicket = true
            } else if (it.startsWith("nearby tickets")) {
                nearbyTickets = true
            } else if (!yourTicket && !nearbyTickets) {
                // valid numbers
                val segments = it.trim().split(":")
                println("${segments.size} in $it")
                val rangeSegment = segments[1].trim()
                val ranges = rangeSegment.split("or")
                ranges.forEach {
                    val firstAndLast = it.trim().split("-")
                    val range = firstAndLast[0].trim().toInt()..firstAndLast[1].trim().toInt()
                    valids.addAll(range)
                }
            } else if (yourTicket && !nearbyTickets) {
                println("yourTicket: $it")
            } else if (nearbyTickets) {
                val numbers = it.trim().split(",").map { it.toInt() }
                numbers.forEach {
                    if (!valids.contains(it)) {
                        error += it
                    }
                }
            }
        }
    }

    println("error: $error")

}

