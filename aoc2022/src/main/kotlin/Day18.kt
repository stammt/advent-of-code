import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day18input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day18sample.txt").readLines()
    day18part2(input)
}

// Part 1: For each cube, check each of it's adjacent neighbors. Each on that is a cube
// means that face is not showing.
// Part 2: Same as part 1, but if there is no adjacent cube, also check to see if that
// space can reach the outside by doing a DFS from the position to see if it can get to
// a position that is outside of the bounds of the existing cubes. This gets super
// expensive in 3 dimensions so cache reachability along the way.

fun day18part2(input: List<String>) {
    val cubes = mutableSetOf<List<Int>>()
    for (line in input) {
        cubes.add(line.split(",").map { it.toInt() })
    }

    val checkedCanReachExterior = mutableMapOf<List<Int>, Boolean>()

    var showing = 0
    for (cube in cubes) {
        var connected = 0
        var interior = 0

        // For each neighbor, if it exists as a cube the side is not showing.
        // Otherwise check to see if it is reachable from outside. If so, the
        // face is "showing" otherwise it is interior and not showing.
        val neighbors = neighbors(cube)
        for (n in neighbors) {
            if (cubes.contains(n)) {
                connected++
            } else if (!canReachExterior(n, cubes, checkedCanReachExterior)) {
                interior++
            }
        }

        val exposed = (6 - connected - interior)
        showing += exposed
    }

    println("Total showing: $showing")
}

fun day18part1(input: List<String>) {
    val cubes = mutableSetOf<List<Int>>()
    for (line in input) {
        cubes.add(line.split(",").map { it.toInt() })
    }

    var showing = 0
    for (cube in cubes) {
        val neighbors = neighbors(cube)
        val connected = neighbors.count { cubes.contains(it) }
        showing += (6 - connected)
    }

    println("Total showing: $showing")
}

fun canReachExterior(start: List<Int>, visited: MutableSet<List<Int>>, cubes: Collection<List<Int>>, checkedCanReachExterior: MutableMap<List<Int>, Boolean>) : Boolean {
    val verbose = false // start == listOf(16, 4, 12) || path.contains(listOf(16, 4, 12))
    visited.add(start)

    if (isOutside(start, cubes)) {
        checkedCanReachExterior[start] = true
        if (verbose) {
            println(">>> $start is outside")
        }
        return true
    }

    val neighbors = neighbors(start)
    for (n in neighbors) {
        if (verbose) {
            println("Checking neighbor $n of $start. isCube: ${cubes.contains(n)}")
        }
        if (!cubes.contains(n) && !visited.contains(n)) {
            if (checkedCanReachExterior.containsKey(n)) {
                if (verbose) {
                    println("**** found cached value for neighbor $n : ${checkedCanReachExterior[n]}")
                }
                return checkedCanReachExterior[n]!!
            }

            val canReachFromNeighbor = canReachExterior(n, visited, cubes, checkedCanReachExterior)
            if (canReachFromNeighbor) {
                if (verbose) {
                    println(">>> found path from $start to outside")
                }
                return true
            }
        }
    }

    if (verbose) {
        println(">>> found NO path to outside")
    }
    return false
}


fun isOutside(cube: List<Int>, cubes: Collection<List<Int>>) : Boolean {
    // return true if the cube is not in the set of cubes, and is out of the range
    // of the cubes.
    if (cubes.contains(cube)) return false

    if (cube[0] < cubes.minOf { it[0] }) return true
    if (cube[0] > cubes.maxOf { it[0] }) return true
    if (cube[1] < cubes.minOf { it[1] }) return true
    if (cube[1] > cubes.maxOf { it[1] }) return true
    if (cube[2] < cubes.minOf { it[2] }) return true
    if (cube[2] > cubes.maxOf { it[2] }) return true

    return false
}

fun canReachExterior(cube: List<Int>, cubes: Collection<List<Int>>, checkedCanReachExterior: MutableMap<List<Int>, Boolean>) : Boolean {
    if (cubes.contains(cube)) {
        println("!!!!! called canReachExterior with a cube $cube")
        return false
    }
    if (isOutside(cube, cubes)) {
        return true
    }
    if (checkedCanReachExterior.containsKey(cube)) {
        return checkedCanReachExterior[cube]!!
    }
    val visited = mutableSetOf<List<Int>>()
    val canReach = canReachExterior(cube, visited, cubes, checkedCanReachExterior)

    // The search traverses nodes that are reachable from one another, so if any of them
    // get to the outside, they can all reach the outside.
    for (node in visited) {
        checkedCanReachExterior[node] = canReach
    }
    return canReach
}

fun neighbors(cube: List<Int>) : Set<List<Int>> {
    val cubes = mutableSetOf<List<Int>>()
    cubes.add(listOf(cube[0] - 1, cube[1], cube[2]))
    cubes.add(listOf(cube[0] + 1, cube[1], cube[2]))
    cubes.add(listOf(cube[0], cube[1] - 1, cube[2]))
    cubes.add(listOf(cube[0], cube[1] + 1, cube[2]))
    cubes.add(listOf(cube[0], cube[1], cube[2] - 1))
    cubes.add(listOf(cube[0], cube[1], cube[2] + 1))
    return cubes
}

fun printSlice(z: Int, cubes: Collection<List<Int>>, checkedCanReachExterior: MutableMap<List<Int>, Boolean>) {
    println("****** z = $z *******")
    for (y in 0..20) {
        print(String.format("%02d", y))
        print(" ")
        for (x in 0..20) {
            val c = listOf(x, y, z)
            val char = if (cubes.contains(c)) {
                '#'
            } else if (!canReachExterior(c, cubes, checkedCanReachExterior)) {
                '@'
            } else {
                '.'
            }
            print(char)
        }
        println()
    }
    println("*********************")
}
