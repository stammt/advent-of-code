import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day08input.txt").readLines()
//    val input = listOf(
//        "30373",
//        "25512",
//        "65332",
//        "33549",
//        "35390",
//    )

    day08part2(input)
}

fun day08part2(input: List<String>) {
    var max = -1

    for (y in input.indices) {
        for (x in input[y].indices) {
            val score = score(x, y, input)
            if (score > max) {
                max = score
            }
        }
    }


    print("max $max")
}

fun score(x: Int, y: Int, input: List<String>) : Int {
    if (x == 0 || y == 0 || x == input[0].length-1 || y == input.size-1) {
        return 0
    }

    val height = input[y][x].digitToInt()

    // look up
    var up = 0
    var i = y - 1
    while (i >= 0) {
        up++
        if (input[i][x].digitToInt() >= height) {
            break
        } else {
            i--
        }
    }
    // look down
    var down = 0
    i = y + 1
    while (i < input.size) {
        down++
        if (input[i][x].digitToInt() >= height) {
            break
        } else {
            i++
        }
    }
    // look left
    var left = 0
    i = x - 1
    while (i >= 0) {
        left++
        if (input[y][i].digitToInt() >= height) {
            break
        } else {
            i--
        }
    }
    // look right
    var right = 0
    i = x + 1
    while (i < input[0].length) {
        right++
        if (input[y][i].digitToInt() >= height) {
            break
        } else {
            i++
        }
    }
    return (up * down * left * right)
}

fun day08part1(input: List<String>) {
    val visible = mutableSetOf<Pair<Int, Int>>()

    println("input length ${input.size} line 0 ${input[0].length}")

    for (y in input.indices) {
        var height = -1
        var x = 0
        while (x < input[y].length /*&& input[y][x].digitToInt() >= height*/) {
//            println("Adding $x , $y")
            if (input[y][x].digitToInt() > height) {
                visible.add(x to y)
                height = input[y][x].digitToInt()
            }
            x++
        }
//        println("line $y ended at $x from left with height $height")

        height = -1
        x = input[y].length - 1
        while (x >= 0 /*&& input[y][x].digitToInt() >= height*/) {
//            println("Adding $x , $y")
            if (input[y][x].digitToInt() > height) {
                visible.add(x to y)
                height = input[y][x].digitToInt()
            }
            x--
        }
//        println("line $y ended at $x from right with height $height")

    }

    for (x in input[0].indices) {
        var height = -1
        var y = 0
        while (y < input.size /*&& input[y][x].digitToInt() >= height*/) {
            if (input[y][x].digitToInt() > height) {
                visible.add(x to y)
                height = input[y][x].digitToInt()
            }
            y++
        }

        height = -1
        y = input.size - 1
        while (y >= 0 /*&& input[y][x].digitToInt() >= height*/) {
            if (input[y][x].digitToInt() > height) {
                visible.add(x to y)
                height = input[y][x].digitToInt()
            }
            y--
        }
    }

    for (y in input.indices) {
        var x = 0
        while (x < input[y].length) {
            if (visible.contains(x to y)) {
                print(input[y][x])
            } else {
                print('x')
            }
            x++
        }
        println("")
    }

    // 633 too low
    println("Visible count: ${visible.size} : $visible")
}

