import java.io.File
import java.lang.Math.floor
import java.time.Duration
import java.time.Instant
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day17input.txt").readLines()
//
//    val input = listOf<String>(".#.",
//    "..#",
//    "###")
    day17Part2(input)
}

fun day17Part2(input: List<String>) {
    // copy into a grid, padded with 6 more spaces in each dimension
    val width = input[0].length + 12
    val height = input.size + 12
    val depth = 13
    val wdepth = 13
    val slices = mutableListOf<MutableList<MutableList<MutableList<Char>>>>()
    for (w in 0 until wdepth) {
        val wslices = mutableListOf<MutableList<MutableList<Char>>>()
        slices.add(wslices)
        for (z in 0 until depth) {
            wslices.add(emptySlice(width, height))
        }
    }

    // initial values
    val initialX = 6
    val initialY = 6
    val initialZ = 6
    val initialW = 6
    for (x in 0 until input[0].length) {
        for (y in 0 until input.size) {
            slices[initialW][initialZ][initialX + x][initialY + y] = input[y][x]
        }
    }

    // for each phase, make a copy, then update the copy based on the
    // previous state
    var previousIteration = slices
    for (iteration in 1..6) {
        println("\n** starting iteration $iteration \n")
        var workingCopy = copySpace4d(previousIteration)

//        println("w 0 to ${previousIteration.size}")
        for (w in 0 until previousIteration.size) {
//            println("z 0 to ${previousIteration[w].size}")
            for (z in 0 until previousIteration[w].size) {
//                println("x 0 to ${previousIteration[w][z].size}")
                for (x in 0 until previousIteration[w][z].size) {
//                    println("y 0 to ${previousIteration[w][z][x].size}")
                    for (y in 0 until previousIteration[w][z][x].size) {
                        val activeNeighborCount = activeNeighborCount4d(w, z, x, y, previousIteration)
                        val previousValue = previousIteration[w][z][x][y]
                        var nextValue = '.'
                        if (previousValue == '#' && (activeNeighborCount == 2 || activeNeighborCount == 3)) {
//                            println("$w $z, $x, $y stays active with $activeNeighborCount")
                            nextValue = '#'
                        } else if (previousValue == '.' && activeNeighborCount == 3) {
//                            println("$w, $z, $x, $y TURNS active with $activeNeighborCount")
                            nextValue = '#'
                        } else if (previousValue != nextValue) {
//                            println("$w, $z, $x, $y is inactive (was $previousValue) with $activeNeighborCount")
                        }


//                        println("setting $w $z $x $y")
                        workingCopy[w][z][x][y] = nextValue
                    }
                }
            }
        }

        previousIteration = workingCopy
    }

    val result = countActiveCells4d(previousIteration)
    println("\n\nActive count: $result")

}

fun day17Part1(input: List<String>) {
    // copy into a grid, padded with 6 more spaces in each dimension
    val width = input[0].length + 12
    val height = input.size + 12
    val depth = 13
    val slices = mutableListOf<MutableList<MutableList<Char>>>()
    for (z in 0 until depth) {
        slices.add(emptySlice(width, height))
    }

    // initial values
    val initialX = 6
    val initialY = 6
    val initialZ = 6
    for (x in 0 until input[0].length) {
        for (y in 0 until input.size) {
            slices[initialZ][initialX + x][initialY + y] = input[y][x]
        }
    }

    // for each phase, make a copy, then update the copy based on the
    // previous state
    var previousIteration = slices
    for (iteration in 1..6) {
        println("\n** starting iteration $iteration \n")
        var workingCopy = copySpace(previousIteration)

        for (z in 0 until previousIteration.size) {
            for (x in 0 until previousIteration[z].size) {
                for (y in 0 until previousIteration[z][x].size) {
                    val activeNeighborCount = activeNeighborCount(z, x, y, previousIteration)
                    val previousValue = previousIteration[z][x][y]
                    var nextValue = '.'
                    if (previousValue == '#' && (activeNeighborCount == 2 || activeNeighborCount == 3)) {
                        println("$z, $x, $y stays active with $activeNeighborCount")
                        nextValue = '#'
                    } else if (previousValue == '.' && activeNeighborCount == 3) {
                        println("$z, $x, $y TURNS active with $activeNeighborCount")
                        nextValue = '#'
                    } else if (previousValue != nextValue) {
                        println("$z, $x, $y is inactive (was $previousValue) with $activeNeighborCount")
                    }



                    workingCopy[z][x][y] = nextValue
                }
            }
        }

        previousIteration = workingCopy
    }

    val result = countActiveCells(previousIteration)
    println("\n\nActive count: $result")

}

fun activeNeighborCount(z: Int, x: Int, y: Int, space: MutableList<MutableList<MutableList<Char>>>) : Int {
    var result = 0

    val debug = false// (z==6 && x==7 && y==8) || (z==6 && x==6 && y==8)

    for (i in (z - 1).coerceAtLeast(0) until (z + 2).coerceAtMost(space.size)) {
        for (j in (x - 1).coerceAtLeast(0) until (x + 2).coerceAtMost(space[z].size)) {
            for (k in (y - 1).coerceAtLeast(0) until (y + 2).coerceAtMost(space[z][x].size)) {
                if (i != z || j != x || k != y) {
                    val char = space[i][j][k]
                    if (debug) {
                        println("$i, $j, $k is $char (neighbor of $z, $x, $y")
                    }
                    if (char == '#') result++
                }
            }
        }
    }

    return result;
}

fun activeNeighborCount4d(w: Int, z: Int, x: Int, y: Int, space: MutableList<MutableList<MutableList<MutableList<Char>>>>) : Int {
    var result = 0

    val debug = false// (z==6 && x==7 && y==8) || (z==6 && x==6 && y==8)

    for (h in (w - 1).coerceAtLeast(0) until (w + 2).coerceAtMost(space.size)) {
        for (i in (z - 1).coerceAtLeast(0) until (z + 2).coerceAtMost(space[w].size)) {
            for (j in (x - 1).coerceAtLeast(0) until (x + 2).coerceAtMost(space[w][z].size)) {
                for (k in (y - 1).coerceAtLeast(0) until (y + 2).coerceAtMost(space[w][z][x].size)) {
                    if (h != w || i != z || j != x || k != y) {
                        val char = space[h][i][j][k]
                        if (debug) {
                            println("$h, $i, $j, $k is $char (neighbor of $w, $z, $x, $y")
                        }
                        if (char == '#') result++
                    }
                }
            }
        }
    }

    return result;
}

fun countActiveCells(space: MutableList<MutableList<MutableList<Char>>>)
        : Int {
    var count = 0
    for (z in 0 until space.size) {
        for (x in 0 until space[z].size) {
            for (y in 0 until space[z][x].size) {
                if (space[z][x][y] == '#') count++
            }
        }
    }

    return count
}

fun countActiveCells4d(space: MutableList<MutableList<MutableList<MutableList<Char>>>>)
        : Int {
    var count = 0

    for (w in 0 until space.size) {
        for (z in 0 until space[w].size) {
            for (x in 0 until space[w][z].size) {
                for (y in 0 until space[w][z][x].size) {
                    if (space[w][z][x][y] == '#') count++
                }
            }
        }
    }

    return count
}


fun copySpace(space: MutableList<MutableList<MutableList<Char>>>)
        : MutableList<MutableList<MutableList<Char>>> {
    val copy = mutableListOf<MutableList<MutableList<Char>>>()

    for (i in 0 until space.size) {
        val rows = mutableListOf<MutableList<Char>>()
        copy.add(rows)
        for (x in 0 until space[i].size) {
            val cols = mutableListOf<Char>()
            rows.add(cols)
            for (y in 0 until space[i][x].size) {
                cols.add(space[i][x][y])
            }
        }
    }

    return copy
}
fun copySpace4d(space: MutableList<MutableList<MutableList<MutableList<Char>>>>)
        : MutableList<MutableList<MutableList<MutableList<Char>>>> {
    val copy = mutableListOf<MutableList<MutableList<MutableList<Char>>>>()

    for (w in 0 until space.size) {
        val ws = mutableListOf<MutableList<MutableList<Char>>>()
        copy.add(ws)
        for (z in 0 until space[w].size) {
            val rows = mutableListOf<MutableList<Char>>()
            ws.add(rows)
            for (x in 0 until space[w][z].size) {
                val cols = mutableListOf<Char>()
                rows.add(cols)
                for (y in 0 until space[w][z][x].size) {
                    cols.add(space[w][z][x][y])
                }
            }
        }
    }

    return copy
}

fun emptySlice(width: Int, height: Int) : MutableList<MutableList<Char>> {
    val cols = mutableListOf<MutableList<Char>>()
    for (x in 0 until width) {
        cols.add(mutableListOf<Char>())
        for (y in 0 until height) {
            cols[x].add('.')
        }
    }
    return cols
}

//fun printCube(cube: List<List<List<Char>>>) {
//    for (z in 0 until cube.size) {
//        println("\n+++ slice $z")
//        for (y in 0 until cube[z][0].size) {
//            println("")
//            for (x in 0 until cube[z].size) {
//                print("${cube[z][x][y]} ")
//            }
//        }
//    }
//
//}