import java.io.File
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day11input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day11sample.txt").readLines()

    day11part1(input)
}


fun day11part1(input: List<String>) {
    val monkeys = parseMonkeys(input)
    val testProduct: ULong = monkeys.map { it.test.toULong() }.reduce(ULong::times)

    for (round in 1..10000) {
        for (monkey in monkeys) {
            val items = monkey.items

            for (item in items) {
                val interest = monkey.op.run(item) % testProduct
//                val zero: ULong = 0u
//                if (interest.mod(monkey.test.toULong()) == ULong.MIN_VALUE) {
//                    monkeys[monkey.testTrue].items.add(interest / monkey.test.toULong())
//                } else {
//                    monkeys[monkey.testFalse].items.add(interest.mod(monkey.test.toULong()))
//                }
                val testResult = if (interest.mod(monkey.test.toULong()) == ULong.MIN_VALUE) monkey.testTrue else monkey.testFalse
                monkeys[testResult].items.add(interest)
                monkey.count++
            }
            monkey.items.clear()
        }
        if (round == 1 || round == 20 || round % 1000 == 0) {
            println("After round $round")
            for (i in monkeys.indices) {
                println("Monkey $i: inspected ${monkeys[i].count}, items: ${monkeys[i].items}")
            }
            println()
        }
    }

    val counts = mutableListOf<Long>()
    for (monkey in monkeys) {
        counts.add(monkey.count)
    }
    counts.sortDescending()
    println("Counts: $counts")
    val result = counts[0] * counts[1]
    println("resuot: $result")
}

fun parseMonkeys(input: List<String>) : List<Monkey> {
    val monkeys = mutableListOf<Monkey>()
    var i = 0
    while (i < input.size) {
        if (input[i].startsWith("Monkey")) {
            i++
            val items = input[i].trim().substring("Starting items: ".length).split(",").map { it.trim().toULong() }
            i++
            val opString = input[i].trim().substring("Operation: new = old ".length).split(" ")
            val op = if (opString[0] == "+") AddOp(opString[1].toULong())
            else if (opString[0] == "*" && opString[1] == "old") SqOp()
            else MulOp(opString[1].toULong())
            i++
            val test = input[i].substringAfterLast(" ").toInt()
            i++
            val ifTrue = input[i].substringAfterLast(" ").toInt()
            i++
            val ifFalse = input[i].substringAfterLast(" ").toInt()

            val monkey = Monkey(items.toMutableList(), op, test, ifTrue, ifFalse)
            println("parsed monkey: $monkey")
            monkeys.add(monkey)
        }
        i++
    }
    return monkeys
}

interface ItemOp {
    fun run(interest: ULong) : ULong
}
class AddOp(private val add: ULong) : ItemOp {
    override fun run(interest: ULong): ULong {
        return interest + add
    }
}
class MulOp(private val mul: ULong) : ItemOp {
    override fun run(interest: ULong): ULong {
//        println("$interest * $mul")
        return interest * mul
    }
}
class SqOp() : ItemOp {
    override fun run(interest: ULong): ULong {
        return interest * interest
//        return interest
    }
}
data class Monkey(val items: MutableList<ULong>, val op: ItemOp, val test: Int, val testTrue: Int, val testFalse: Int) {
    var count = 0L
}
