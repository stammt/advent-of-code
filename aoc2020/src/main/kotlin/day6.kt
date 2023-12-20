import java.io.File
import kotlin.math.floor

fun main(args: Array<String>) {
    val fileLines = File("/Users/stammt/dev/aoc/day6input.txt").readLines()
//    day6part1(fileLines) //6809
    day6part2(fileLines)
}

fun day6part2(fileLines: List<String>) {
//    var answers = mutableListOf<Set<Char>>()

    var count = 0
    var currentGroup = mutableMapOf<Char, Int>()
    var groupSize = 0;
//    answers.add(currentSet)
    fileLines.forEach {
        var line = it.trim()
        if (line.length == 0) {
            currentGroup.keys.forEach{
                if (currentGroup[it] == groupSize) {
                    count++
                }
            }
            println("group had $groupSize $currentGroup")

            currentGroup = mutableMapOf<Char, Int>()
            groupSize = 0;
        } else {
            groupSize++
            line.forEach {
                var x = currentGroup[it] ?: 0
                currentGroup[it] = x + 1
            }
        }
    }
    currentGroup.keys.forEach{
        if (currentGroup[it] == groupSize) {
            count++
        }
    }

    println("$count questions")
}

fun day6part1(fileLines: List<String>) {
    var answers = mutableListOf<Set<Char>>()

    var currentSet = mutableSetOf<Char>()
    answers.add(currentSet)
    fileLines.forEach {
        var line = it.trim()
        if (line.length == 0) {
            currentSet = mutableSetOf<Char>()
            answers.add(currentSet)
        } else {
            currentSet.addAll(line.toList())
        }
    }

    var count = 0
    answers.forEach{count += it.size}

    println("${answers.size} groups and $count questions")
}
