import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.ceil
import kotlin.math.floor

fun main(args: Array<String>) {
    val fileinput = File("/Users/stammt/Documents/dev/advent-of-code/aoc2021/input/day24input.txt").readLines()

    val sample1 = ("inp x\n" +
            "mul x -1").split("\n")

    val sample2 = ("inp z\n" +
            "inp x\n" +
            "mul z 3\n" +
            "eql z x").split("\n")

    val sample3 = ("inp w\n" +
            "mul w -1\n" +
            "mod w 2\n" +
            "div x -2").split("\n")

    val bin = ("inp w\n" +
            "add z w\n" +
            "mod z 2\n" +
            "div w 2\n" +
            "add y w\n" +
            "mod y 2\n" +
            "div w 2\n" +
            "add x w\n" +
            "mod x 2\n" +
            "div w 2\n" +
            "mod w 2").split("\n")

    val start = System.nanoTime()
    val largest = generate(0, 0, 0, intArrayOf(9, 8, 7, 6, 5, 4, 3, 2, 1))
    // 52926995971999
    println("largest: $largest")
    val smallest = generate(0, 0, 0, intArrayOf(1, 2, 3, 4, 5, 6, 7, 8, 9))
    println("smallest: $smallest")
    val end = System.nanoTime()
    val time = (end - start) / 1_000_000
    println("took $time ms")
}

// div z A
val A = intArrayOf(1,  1,  1,  26,  1,  1, 1, 26,  1,  26,  26,  26, 26,  26)
// add x B
val B = intArrayOf(10, 12, 15, -9, 15, 10, 14, -5, 14, -7, -12, -10, -1, -11)
// add y C
val C = intArrayOf(15,  8,  2,   6, 13,  4,  1,  9,  5, 13,   9,   6,  2,   2)

val KNOWN_BAD = mutableSetOf<Pair<Int, Int>>()

/**
 * Do a DFS to try numbers 1-9 in each position and see where we end up with z==0 first.
 */
fun generate(depth: Int, modelNumber: Long, zzz: Int, digits: IntArray): Long? {

    if (KNOWN_BAD.contains(Pair(depth, zzz)) || depth == 14) {
        return null
    }

//    println("Checking from $modelNumber")
    val updatedNumber = modelNumber * 10
    for (i in digits.indices) {
        var z = zzz
        val w = digits[i]
        var x = z
        x %= 26
        z /= A[depth]
        x += B[depth]
        x = if (x == w) 1 else 0
        x = if (x == 0) 1 else 0
        var y = 0
        y += 25
        y *= x
        y += 1
        z *= y
        y = w
        y += C[depth]
        y *= x
        z += y

        if (z == 0 && depth == 13) {
            return updatedNumber + digits[i]
        }
        val result = generate(depth + 1, updatedNumber + digits[i], z, digits)
        if (result != null) {
            return result
        }
    }
    KNOWN_BAD.add(Pair(depth, zzz))
    return null
}



/***
 * x = ((z % 26) + I) == input) ? 0 : 1
 * z = (z // J) * ((25 * x) + 1) # x will always be 0 or 1
 * z = z + (input + K)
 *
 * I, J, K
 * 10, 1, 15
 * 12, 1, 8
 * 15, 1, 2
 * -9, 26, 6
 * 15, 1, 13
 * 10, 1, 4
 * 14, 26, 1
 * -5, 26, 9
 * 14, 1, 5
 * -7, 26, 13
 * -12, 26, 9
 * -10, 26, 6
 * -1, 26, 2
 * -11, 26, 2
 *
 * Work backwards from z = 0
 * x = ((z % 26) - 11) == input ? 0 : 1
 * z = (z // 26) * ((25 * x) + 1) -- either z or z // 26
 * 0 = z + input + 2
 *
 *
 * input 1 into w:
 * put z in x (z will be 0)
 * x = (x % 26) + 10
 * if x == w, x = 0 (from:)
 *     if x == w, x = 1, else x = 0
 *     if x == 0, x = 1 else x = 0
 * y = (25 * x) + 1
 * z = z * y
 * y = (w + 15) * x
 * z = z + y
 *
 * input 2 into w:
 * x = (z % 26) + 12
 * if x == w, x = 0 (from:)
 *     if x == w, x = 1, else x = 0
 *     if x == 0, x = 1 else x = 0
 * y = (25 * x) + 1
 * z = z * y
 * y = (w + 8) * x
 * x = z + y
 *
 * input 3 into w:
 * x = (z % 26) + 15
 * if x == w, x = 0 (from:)
 *     if x == w, x = 1, else x = 0
 *     if x == 0, x = 1 else x = 0
 * y = (25 * x) + 1
 * z = z * y
 * y = (w + 2) * x
 * z = z + y
 *
 * input 4 into w:
 * x = (z % 26) - 9
 * z = z // 26
 * if x == w, x = 0 (from:)
 *     if x == w, x = 1, else x = 0
 *     if x == 0, x = 1 else x = 0
 * y = (25 * x) + 1
 * z = z * y
 * y = (w + 6) * x
 * z = z + y
 */
