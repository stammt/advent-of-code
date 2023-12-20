import java.io.File
import java.lang.Math.floor
import java.time.Duration
import java.time.Instant
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day18input.txt").readLines()
    day18Part1(input)
}

interface MathExpression {
    open val op: Char
    open val right: MathExpression
    open val left: MathExpression
    open val grouped: Boolean

    open fun getValue() : Long
}

class MathValue(private val value: Long) : MathExpression {
    override val op = ' '
    override val right = this
    override val left = this
    override val grouped = true

    override fun getValue(): Long {
        return value
    }
    override fun toString() : String {
        return " $value "
    }
}

class MathOperation(override val op: Char,  override val left: MathExpression,  override val right: MathExpression, override val grouped: Boolean = false) : MathExpression {
    override fun getValue() : Long {
        val leftValue = left.getValue()
        val rightValue = right.getValue()
        return when (op) {
            '+' -> leftValue + rightValue
            '*' -> leftValue * rightValue
            else -> -1
        }
    }
    override fun toString() : String {
        return " ($left $op $right $grouped {${getValue()}})"
    }
}

fun buildExpression(input: CharArray) : MathExpression {
    var hasLeft = false
    var hasRight = false
    var hasOp = false
    var left: MathExpression = MathValue(0L)
    var right: MathExpression = MathValue(0L)
    var op: Char = '+'
    var i = 0
    while (i < input.size) {
        if (input[i] == ' ') {
            i++
            continue
        }

//        println("$i : ${input[i]}")
        if (input[i] == '+' || input[i] == '*') {
            op = input[i]
            i++
            hasOp = true
        } else if (!hasLeft || !hasRight) {
            var expr: MathExpression
            if (input[i] == '(') {
                var openCount = 1
                var end = -1
                for (j in (i+1) until input.size) {
                    if (input[j] == '(') openCount++
                    else if (input[j] == ')') openCount--
                    if (openCount == 0) {
                        end = j
                        break
                    }
                }
                if (openCount != 0) {
                    println("!!! found unbalanced parens starting at $i")
                }
                expr = buildExpression(input.copyOfRange(i + 1, end))
                i = end+1
            } else {
                expr = MathValue(("" + input[i]).toLong())
                i++
            }
            if (!hasLeft) {
                left = expr
                hasLeft = true
            } else if (!hasRight) {
                right = expr
                hasRight = true
            }
        }
        if (hasLeft && hasOp && hasRight) {
//            println("building $op $left $right")
            left = MathOperation(op, left, right)
            hasOp = false
            hasRight = false
        }
    }
    return left
}

fun buildExpression2(input: CharArray, grouped: Boolean = false) : MathExpression {
    var hasLeft = false
    var hasRight = false
    var hasOp = false
    var left: MathExpression = MathValue(0L)
    var right: MathExpression = MathValue(0L)
    var op: Char = '+'
    var i = 0
    while (i < input.size) {
        if (input[i] == ' ') {
            i++
            continue
        }

//        println("$i : ${input[i]}")
        if (input[i] == '+' || input[i] == '*') {
            op = input[i]
            i++
            hasOp = true
        } else if (!hasLeft || !hasRight) {
            var expr: MathExpression
            if (input[i] == '(') {
                var openCount = 1
                var end = -1
                for (j in (i+1) until input.size) {
                    if (input[j] == '(') openCount++
                    else if (input[j] == ')') openCount--
                    if (openCount == 0) {
                        end = j
                        break
                    }
                }
                if (openCount != 0) {
                    println("!!! found unbalanced parens starting at $i")
                }
                expr = buildExpression2(input.copyOfRange(i + 1, end), true)
                i = end+1
            } else {
                expr = MathValue(("" + input[i]).toLong())
                i++
            }
            if (!hasLeft) {
                left = expr
                hasLeft = true
            } else if (!hasRight) {
                right = expr
                hasRight = true
            }
        }
        if (hasLeft && hasOp && hasRight) {
            // If we encounter an addition operation and the left side is a multiplication that is not
            // grouped, swap things around to give the addition precedence
            if (op == '+' && left.op == '*' && !left.grouped) {
                right = MathOperation('+', left.right, right, false)
                left = MathOperation('*', left.left, right, false)
            } else {
                left = MathOperation(op, left, right, false)
            }
            hasOp = false
            hasRight = false
        }
    }

    // If this expression is grouped, rebuild it with that flag so we won't break it up later
    if (grouped) {
        left = MathOperation(left.op, left.left, left.right, true)
    }
    return left
}

fun day18Part1(input: List<String>) {
//    val line = "1 + 2 * 3 + 4 * 5 + 6"
//    val line = "1 + (2 * 3) + (4 * (5 + 6))"
//    val line = "2 * 3 + (4 * 5)"
//    val line = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
//    val line = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
//    val line = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
//    val expr = buildExpression2(line.toCharArray())
//    println("result: ${expr.toString()} => ${expr.getValue()}")

    var sum = 0L
    input.forEach {
        val expr = buildExpression2(it.toCharArray())
        sum += expr.getValue()
    }
    // 1812190034617954 is too high
    // 283729053022731 right!
    println("sum = $sum")
}
