import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day21input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day21sample.txt").readLines()
    day21part2(input)
}

fun day21part2(input: List<String>) {
    val monkeys = parseYellingMonkeys(input)
    println(monkeys)

    val values = mutableMapOf<String, MonkeyExpression>()
    val q = mutableListOf("root")
    var result = 0L
    while (q.isNotEmpty()) {
        val next = monkeys[q.first()]!!
        val needs = next.needs(values)
        if (needs.isEmpty()) {
            if (next.name() == "root") {
                // Special case, unwind the tree
                val rootExpr = next.yell(values) as HumanExpr
                println("Root: $rootExpr")

                result = HumanExpr(rootExpr.e1, rootExpr.e2, "=").eval(0)

            } else {
                values[next.name()] = next.yell(values)
            }
            q.removeFirst()
        } else {
            for (n in needs) {
                q.add(0, n)
            }
        }
    }

    // 9910093046258 too high
    println("Result: ${result}")
}


fun day21part1(input: List<String>) {
    val monkeys = parseYellingMonkeys(input)
    println(monkeys)

    val values = mutableMapOf<String, MonkeyExpression>()
    val q = mutableListOf("root")
    while (q.isNotEmpty()) {
        val next = monkeys[q.first()]!!
        val needs = next.needs(values)
        if (needs.isEmpty()) {
            values[next.name()] = next.yell(values)
            q.removeFirst()
        } else {
            for (n in needs) {
                q.add(0, n)
            }
        }
    }

    // 897441886 too low
    // 3916491093941 too high
    // 3916491093817 yes!
    println("Root: ${values["root"]}")
}

fun parseYellingMonkeys(input: List<String>) : Map<String, YellingMonkey>{
    val monkeys = mutableMapOf<String, YellingMonkey>()
    for (line in input) {
        val name = line.split(":")[0]
        val v = line.split(": ")[1]
        if (name == "humn") {
            monkeys[name] = Human()
        } else if (v.all { it.isDigit() }) {
            monkeys[name] = ValueMonkey(name, ExprLiteral (v.toLong()))
        } else {
            val (v1, op, v2) = v.split(" ")
            monkeys[name] = OpMonkey(name, v1, v2, op)
        }
    }
    return monkeys
}

interface MonkeyExpression {
    fun eval(root: Long) : Long
}

class UnknownExpr : MonkeyExpression {
    override fun eval(root: Long): Long {
        println("unknown is $root")
        return root
    }
}

data class ExprLiteral(val value: Long) : MonkeyExpression {
    override fun eval(root: Long) : Long {
        return value
    }
}

data class HumanExpr(val e1: MonkeyExpression, val e2: MonkeyExpression, val op: String) : MonkeyExpression {
    override fun eval(root: Long) : Long {
        // one side will be a literal, the other side will have the human value
        // take the value we're trying to equal (from root)
        // apply reverse op to the root value and the literal, that will
        // now equal the human value
        // Repeat/recurse until we just have a human value.

        val number: ExprLiteral = if (e1 is ExprLiteral) e1 else (e2 as ExprLiteral)
        val humanEquation = if (e2 is ExprLiteral) e1 else e2
//        println("number: $number : $humanEquation")

        if (op == "=") {
            println("Start solving: ${number.value} equals $humanEquation")
            return humanEquation.eval(number.value)
        }

        println("Solving $root = $e1 $op $$e2")

        val modified = if (op == "+") {
            root - number.value
        } else if (op == "-") {
            if (number == e1) {
                0 - (root - number.value)
            } else {
                println("root plus number: ${root + number.value}")
                root + number.value
            }
        } else if (op == "*") {
            root / number.value
        } else if (op == "/") {
//            root * number.value
            if (number == e1) {
                number.value / root
            } else {
                number.value * root
            }
        } else {
            throw IllegalArgumentException("Unknown op $op")
        }

        return humanEquation.eval(modified)
    }
}



interface YellingMonkey {
    fun yell(values: Map<String, MonkeyExpression>) : MonkeyExpression
    fun needs(values: Map<String, MonkeyExpression>) : List<String>
    fun name() : String
}

class Human : YellingMonkey {
    override fun yell(values: Map<String, MonkeyExpression>): MonkeyExpression {
        return UnknownExpr()
    }

    override fun needs(values: Map<String, MonkeyExpression>): List<String> {
        return listOf()
    }

    override fun name(): String {
        return "humn"
    }

}

data class ValueMonkey(val name: String, val value: MonkeyExpression) : YellingMonkey{
    override fun yell(values: Map<String, MonkeyExpression>) : MonkeyExpression {
        return value
    }

    override fun needs(values: Map<String, MonkeyExpression>) : List<String> {
        return listOf()
    }

    override fun name() : String {
        return name
    }
}

data class OpMonkey(val name: String, val v1: String, val v2: String, val op: String) : YellingMonkey {
    override fun yell(values: Map<String, MonkeyExpression>) : MonkeyExpression {
        // If both are literals, just do the operation
        // Otherwise build a subtree and return that
        val v1Exp = values[v1]!!
        val v2Exp = values[v2]!!
        if (v1Exp is ExprLiteral && v2Exp is ExprLiteral) {
            val v1Int = v1Exp.value
            val v2Int = v2Exp.value
            val result = if (op == "+") {
                v1Int + v2Int
            } else if (op == "-") {
                v1Int - v2Int
            } else if (op == "*") {
                v1Int * v2Int
            } else if (op == "/") {
                v1Int / v2Int
            } else {
                throw IllegalArgumentException("Unknown op $op")
            }
            return ExprLiteral(result)
        } else {
            return HumanExpr(v1Exp, v2Exp, op)
        }
    }

    override fun needs(values: Map<String, MonkeyExpression>) : List<String> {
        val n = mutableListOf<String>()
        if (!values.containsKey(v1)) {
            n.add(v1)
        }
        if (!values.containsKey(v2)) {
            n.add(v2)
        }
        return n
    }

    override fun name() : String {
        return name
    }

}