import java.io.File
import java.lang.Math.floor
import java.time.Duration
import java.time.Instant
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day19input.txt").readLines()
//    val input = File("/Users/stammt/dev/aoc/day19sampleAll.txt").readLines()

//    val input = listOf<String>( "0: 4 1 5",
//    "1: 2 3 | 3 2",
//        "2: 4 4 | 5 5",
//        "3: 4 5 | 5 4",
//        "4:\"a\"",
//        "5: \"b\"",
//        "",
//        "ababbb",
//        "bababa",
//        "abbbab",
//        "aaabbb",
//        "aaaabbb");
    day19Part1(input)
}

interface Rule {
    open fun matches(input: String, rules: Map<Int, Rule>) : Boolean

    // the input length that might match this rule. For loop rules this is the
    // minimum, base case input length
    open fun matchLength(rules: Map<Int, Rule>) : Int
}

class LiteralRule(private val s : String) : Rule {
    override fun matches(input: String, rules: Map<Int, Rule>): Boolean {
//        println("matching $input to literal $s")
        return input.equals(s)
    }

    override fun matchLength(rules: Map<Int, Rule>): Int {
        return s.length
    }

    override fun toString(): String {
        return "\"$s\""
    }
}

class OrRule(private val r1 : Rule, private val r2 : Rule) : Rule {
    override fun matches(input: String, rules: Map<Int, Rule>): Boolean {
//        println("matching $input to or $this")
        return r1.matches(input, rules) || r2.matches(input, rules)
    }

    override fun matchLength(rules: Map<Int, Rule>): Int {
        return r1.matchLength(rules).coerceAtMost(r2.matchLength(rules))
    }

    override fun toString(): String {
        return "($r1 | $r2)"
    }
}

class SequenceRule(val seq: List<Rule>) : Rule {
    override fun matches(input: String, rules: Map<Int, Rule>): Boolean {
//        println("matching $input to sequence $this")
        var start = input.length
        var end = input.length
        var r = 0
        var matched = 0
        for (i in (seq.size - 1) downTo 0) {
            // we know how long each rule should be, so split the string and just
            // match that substring; then match the next rule to the next substring, etc.
            // If this is a loop rule, try matching any number of loops until we either
            // get a match or run out of input. Start with the max number of loops based
            // on the input length to consume as much input as possible.

            var rule = seq[i]
            if (rule is SingleRule) {
                val referencedRule = rules[(rule as SingleRule).id]
                if (referencedRule is LoopRule) {
                    rule = referencedRule
                }
            }
            val ruleLength = rule.matchLength(rules)

            if (rule is LoopRule) {
                var maxLoops = end / ruleLength
                start = end % ruleLength

                var loops = 0
                var matchedLoop = false
                while (!matchedLoop && ++loops <= maxLoops) {
//                    println("checking loop $loops")

                    if (rule.matches(input.substring(start, end), rules)) {
                        matchedLoop = true
                        break
                    } else if (loops < maxLoops) {
                        start += ruleLength
                    }
                }
                if (matchedLoop) {
                    matched++
                    end = start
                } else {
                    break
                }

            } else {
                start -= ruleLength
                if (start < 0) break

                if (!rule.matches(input.substring(start, end), rules)) {
                    break
                }
                matched++
                end = start
            }
        }

        val matchedAll = (matched == seq.size) && (start == 0)
//        println("$matchedAll : $input matched $seq ($matched $start)")
        return matchedAll
    }

    override fun matchLength(rules: Map<Int, Rule>): Int {
        var len = 0
        seq.forEach { len += it.matchLength(rules) }
        return len
    }

    override fun toString(): String {
        return "($seq)"
    }
}

// rule that references another rule by numeric ID
class SingleRule( val id: Int) : Rule {
    override fun matches(input: String, rules: Map<Int, Rule>): Boolean {
        val r = rules[id]
        if (r == null) {
            println("didn't find rule $id !!")
            return false
        }

//        println("matching single rule $id ($r) to  $input")
        return r.matches(input, rules)
    }

    override fun matchLength(rules: Map<Int, Rule>): Int {
        return rules[id]?.matchLength(rules)!!
    }

    override fun toString(): String {
        return "($id)"
    }
}

class SelfReferenceRule(val id: Int) : Rule {
    override fun matches(input: String, rules: Map<Int, Rule>): Boolean {
        return true
    }

    override fun matchLength(rules: Map<Int, Rule>): Int {
        return 0
    }

    override fun toString(): String {
        return "(self $id)"
    }
}

class LoopRule(val r1: Rule, val r2: Rule, val id: Int) : Rule {
    override fun matches(input: String, rules: Map<Int, Rule>): Boolean {
        // see how many loops are expected based on the input length
        val baseLength = matchLength(rules)
        val loops = input.length / baseLength
        val loopRule: SequenceRule = when (containsLoop(r1)) {
            true -> r1 as SequenceRule
            else -> r2 as SequenceRule
        }
        val baseRule = when (containsLoop(r1)) {
            true -> r2
            else -> r1
        }

        var rule: Rule
        if (loops == 1) {
            rule = baseRule
//            println("Rule $id with one loop is  ($rule)")
        } else {
            // for each loop, iteratively swap out the self reference rule with
            // the base rule
            val rules = mutableListOf<Rule>()
            rules.addAll(loopRule.seq)
            for (i in 1 until loops) {
                val insert = mutableListOf<Rule>()
                insert.addAll(loopRule.seq)
                val replaceIndex = rules.indexOfFirst { it is SelfReferenceRule }
                rules.removeAt(replaceIndex)
                rules.addAll(replaceIndex, insert)
            }

            val replaceIndex = rules.indexOfFirst { it is SelfReferenceRule }
            rules.removeAt(replaceIndex)
            rule = SequenceRule(rules)

//            println("Rule $id with $loops loops is now ($rule)")
        }

        return rule.matches(input, rules)
    }

    override fun matchLength(rules: Map<Int, Rule>): Int {
        // return the length of the rule without the self reference
        return when (containsLoop(r1)) {
            true -> r2.matchLength(rules)
            else -> r1.matchLength(rules)
        }
    }

    private fun containsLoop(r: Rule) : Boolean {
        return (r is SequenceRule) && r.seq.any { it is SelfReferenceRule }
    }
}

fun createRule(input: String, id: Int) : Rule {
    val rules = input.trim().split("|")
    if (rules.size == 2) {
        val r1 = createRule(rules[0].trim(), id)
        val r2 = createRule(rules[1].trim(), id)
        if (rules[0].trim().split(" ").contains("$id")
            || rules[1].trim().split(" ").contains("$id")) {
                println("creating loop rule for $id")
            return LoopRule(r1, r2, id)
        } else {
            return OrRule(r1, r2)
        }
    }

    val parts = input.trim().split(" ")
    if (parts.size > 1) {
        val rules = parts.map{ createRule(it.trim(), id) }
        return SequenceRule(rules)
    }

    if (input.trim().startsWith("\"") && input.endsWith("\"")) {
        return LiteralRule(input.trim().substring(1, input.length - 1))
    }

    // Sentinel rule type for replacement in loop rules
    if (input.trim().toInt() == id) {
        return SelfReferenceRule(id)
    }

    return SingleRule(input.trim().toInt())
}

fun day19Part1(input: List<String>) {
    var startTime = System.currentTimeMillis()
    var i = 0
    var startedInputs = false
    val ruleMap = mutableMapOf<Int, Rule>()
    var count = 0
    while (i < input.size) {
        val line = input[i].trim()
        if (line.isNullOrEmpty()) {
            println("starting inputs")
            startedInputs = true
        } else if (!startedInputs) {
            val topLevels = line.split(":")
            val ruleId = topLevels[0].toInt()
            println("parsing rule $ruleId from $line")
            val rule = createRule(topLevels[1].trim(), ruleId)
            ruleMap[ruleId] = rule
        } else {
            val zero = ruleMap[0] ?: LiteralRule("")
            println("\n\n1. matching $line to $zero")
            val matches = zero.matches(line, ruleMap)
            println("matches $matches : $line")
            if (matches) {
                count++
            }
        }
        i++
    }

    var endTime = System.currentTimeMillis()

    // 287
    println("Matches $count in ${endTime - startTime}ms")
}



//class RuleZero : Rule {
//    override fun matches(input: String, rules: Map<Int, Rule>): Boolean {
//        // Special case - matches any number of rule 42 (expanded from rule 8), followed by
//        // (N * rule 42 followed by N * rule 31) (expanded from rule 11)
//
//        val rule42  = rules[42]!!
//        val rule31 = rules[31]!!
//        val rule42Len = rule42.matchLength(rules)
//        val rule31len = rule31.matchLength(rules)
//        val rule11Len = rule42Len + rule31len
//
//        // work backwards, see if we can match rule 11 at the end first, because rule
//        // 11 starts with rule 42, and rule 8 ends with rule 42 and we need to figure
//        // out where the dividing point is.
//        var end = input.length
//        var start = 0
//        var rule11Loops = 1
//        var matchedRule11 = false
//        do {
//            start = end - (rule11Len * (rule11Loops))
//            if (start < 0) break
//
//            println("RuleZero: checking rule11 starting at $start ($rule11Loops): ${input.substring(start)}")
//
//            // create a new sequence rule with the right number of loops. Keep going
//            // until we run out of input or it matches.
//            val seq = mutableListOf<Rule>()
//            for (i in 0 until rule11Loops) {
//                seq.add(0, rule42)
//                seq.add(rule31)
//            }
//            val rule = SequenceRule(seq)
//            if (rule.matches(input.substring(start), rules)) {
//                matchedRule11 = true
//                break
//            } else {
//                rule11Loops++
//            }
//        } while (start >= 0)
//
//        if (!matchedRule11) {
//            println("RuleZero: didn't match any rule11 in $input")
//            return false
//        }
//
//        // then see if we can match a series of rule 42 from the beginning to
//        // the start of the rule 11 loops
//        end = input.length - (rule11Len * rule11Loops)
//        val rule42input = input.substring(0, end)
//
//        println("RuleZero: looking for rule42 loops in $rule42input ($input up to $end")
//        val rule42Loops = rule42input.length / rule42Len
//        if (rule42Loops == 0) {
//            println("RuleZero: No room for rule42")
//            return false
//        }
//        println("RuleZero: rule42Len $rule42Len out of ${rule42input.length} is $rule42Loops")
//
//        val seq = mutableListOf<Rule>()
//        for (i in 0 until rule42Loops) seq.add(rule42)
//        val rule = SequenceRule(seq)
//        if (rule.matches(rule42input, rules)) {
//            println("RuleZero: matched $rule42Loops !")
//            return true
//        } else {
//            println("RuleZero: rule42 match failed")
//            return false
//        }
//
//    }
//
//    override fun matchLength(rules: Map<Int, Rule>): Int {
//        return 0
//    }
//
//    override fun toString(): String {
//        return "(RuleZero)"
//    }
//}
