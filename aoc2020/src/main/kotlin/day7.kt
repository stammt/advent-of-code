import java.io.File
import kotlin.math.floor

fun main(args: Array<String>) {
    val fileLines = File("/Users/stammt/dev/aoc/day7input.txt").readLines()
    day7part2(fileLines)
}

fun day7part2(fileLines: List<String>) {
    val rules = mutableMapOf<String, MutableList<String>>()
    fileLines.forEach{
        addRule(rules, it)
    }

    var count = countContents(rules, "shiny gold")
    print("$count bags in shiny gold")
}

fun countContents(rules: MutableMap<String, MutableList<String>>, color: String) : Int {
    val contents = rules[color] ?: listOf()
    var count = 0
    contents.forEach {
        count++
        count += countContents(rules, it)
    }
    return count
}

fun day7part1(fileLines: List<String>) {
    val rules = mutableMapOf<String, MutableList<String>>()
    fileLines.forEach{
        addRule(rules, it)
    }

    var count = 0
    rules.forEach{
        val color = it.key
        if (canReach(rules, color, "shiny gold")) count++
    }
    print("$count colors can reach shiny gold")
}

fun canReach(rules: MutableMap<String, MutableList<String>>, start: String, target: String) : Boolean {
    val contents = rules[start] ?: return false
    val uniqueContents = contents.toSet()

    if (uniqueContents.contains(target)) return true
    uniqueContents.forEach {
        if (canReach(rules, it, target)) return true
    }
    return false
}

fun addRule(rules: MutableMap<String, MutableList<String>>, rule: String) {
    println("** parsing rule $rule")
    var trimmedRule = rule.trim()
    if (trimmedRule.endsWith(".")) {
        trimmedRule = trimmedRule.substring(0, rule.length - 1)
    }
    val segments = trimmedRule.split("contain")
    var color = segments[0].trim()
    if (color.endsWith("bags")) {
        color = color.substring(0, color.length - "bags".length).trim()
    }

    val entry = rules[color] ?: mutableListOf<String>()
    val contents = segments[1].trim().split(",")
    contents.forEach{
        if (!it.trim().equals("no other bags")) {
            //"1 bright white bag"
            val parts = it.trim().split(" ")
            val count = parts[0].toInt()
            val color = parts.subList(1, parts.size - 1).joinToString(" ")
            for (i in 0 until count) {
                entry.add(color)
            }
        }
    }
    rules[color] = entry
    println("$color -> $entry")
}