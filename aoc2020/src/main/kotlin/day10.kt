import java.io.File
import java.time.Duration
import java.time.Instant

fun main(args: Array<String>) {
    val lines = File("/Users/stammt/dev/aoc/day10input.txt").readLines()
    val numbers = ArrayList<Int>()
    //val inputs = input.map(String::toInt).sorted().toMutableList()
    lines.forEach {
        numbers.add(it.toInt())
    }
//    val numbers = mutableListOf(16,
//        10,
//        15,
//        5,
////        13L,
//        1,
//        11,
//        7,
//        19,
//        6,
//        12,
//        18,
//        4)
    numbers.add(0)
    numbers.sort()
    numbers.add(numbers[numbers.size - 1] + 3)

    println("allSOrted $numbers")

    val result = part2(numbers)
    part2b(numbers)
    println("result $result")
    // WRONG 567557012
    // right: 21156911906816
}

private fun part2b(inputs : List<Int>) {
//    val input = testInput
//    val input = test2
//    val input = realInput
//
//    val inputs = input.map(String::toInt).sorted().toMutableList()

//    inputs.add(0, 0)
//    inputs.add(inputs.last() + 3)

    val start = Instant.now()
    var currentRun = 0
    var product = 1L

    var last = -3

    inputs.forEach { v ->
        val diff = v - last
        last = v
        if (diff == 1) {
            currentRun++
        } else {
            val r = when (currentRun) {
                0 -> 1
                1 -> 1
                2 -> 2
                3 -> 4
                4 -> 7
                else -> throw Exception()
            }
            if (r > 1) {
                product *= r
            }
            currentRun = 0
        }
    }

    val end = Instant.now()
    val duration = Duration.between(start, end)
    println("useconds: ${duration.toNanos() / (1000)}")
    println(product)
}

fun part2(numbers: List<Int>) : Long {
    // build a list of count of potential paths from each adapter
    val pathsFromAdapter = mutableListOf<Long>()
    for (i in 0..(numbers.size - 1)) {
        pathsFromAdapter.add(0L)
    }

    // initialize last adapter to have one path
    pathsFromAdapter[numbers.size - 1] = 1L;

    // walk backwards through the list, starting from second-to-last
    // adapter. Each adapter's count of potential paths is the sum of
    // potential paths from the adapters that the current one can
    // go to.
    var i = numbers.size - 2

    do {
        var check = i+1;
        var pathsFromIndex = 0L;
        val jolts = numbers[i]
        // check the next adapters, and add the path counts for ones that are
        // less than 3 jolts away from the current adapter
        while ((check < numbers.size) && (numbers[check] - jolts <= 3)) {
            pathsFromIndex += pathsFromAdapter[check]
            check++
        }

        // cache the number of paths from this adapter so we can
        // add it in later if we need to
        pathsFromAdapter[i] = pathsFromIndex
    } while (--i >= 0)

    return pathsFromAdapter[0]
}

fun part2xxxzzx(numbers: List<Long>) : Double {
    // at each index, how many paths?
    var pathsPerIndex = mutableListOf<Long>()
    val count = numbers.size - 1
    for (i in 0..count) {
        var paths = 0L;
        if (i < count && numbers[i+1] - numbers[i] <= 3L) {
            paths++;
        }
        if (i < count - 1 && numbers[i+2] - numbers[i] <= 3L) {
            paths++;
        }
        if (i < count - 2 && numbers[i+3] - numbers[i] <= 3L) {
            paths++;
        }
        if (i == count) {
            paths = 1
        }
        pathsPerIndex.add(paths)
    }
    println("pathsPerIndex: $pathsPerIndex")

    val combinationsFromIndex = ArrayList<Long>()
    for (i in 0..count) {
        combinationsFromIndex.add(combinationsFrom(pathsPerIndex, i))
    }
    println("combinationsFromIndex: $combinationsFromIndex")

    val pathsToEnd = mutableListOf<Long>()
    for (i in 0..count) {
        pathsToEnd.add(1L)
    }

    var current = numbers.size
    var pathCount = 1;
    while (--current >= 0) {
        if (pathsPerIndex[current] == 1L) {
            if (current < numbers.size - 1) {
                pathsToEnd[current] = pathsToEnd[current + 1]
            }
        } else {

        }
    }


    var allPaths = 0L
    for (i in 0..count) {
        if (pathsPerIndex[i] > 1) {
            var paths = 0L
            if (i < count && numbers[i + 1] - numbers[i] <= 3L) {
                paths += combinationsFromIndex[i + 1];
            }
            if (i < count - 1 && numbers[i + 2] - numbers[i] <= 3L) {
                paths += combinationsFromIndex[i + 2];
            }
            if (i < count - 2 && numbers[i + 3] - numbers[i] <= 3L) {
                paths += combinationsFromIndex[i + 3];
            }
            println("found $paths paths from $i")
            allPaths += paths
        }
    }
    println("allPaths: $allPaths")

//    var paths: Double = 1.0
//    for (i in count..0) {
//        paths = Math.pow(paths, pathsPerIndex[i].toDouble())
//    }
//    println("paths: $paths")
    return 1.0
}

fun combinationsFrom(pathsPerIndex: List<Long>, from: Int) : Long {
    val max = pathsPerIndex.size - 1;
    var combinations = pathsPerIndex[from];
    for (i in (from+1)..max) {
        combinations *= pathsPerIndex[i]
    }
    return combinations
}

fun part2x(numbers: List<Long>, start: Int) : Int {
    if (start == numbers.size - 1) return 1
    if (start > numbers.size - 1) {
        println("uh oh, got start of $start out of ${numbers.size}")
        return 0
    }

    var paths = 0
    val jolts = numbers[start]
    if (((start + 1) < numbers.size) && (numbers[start + 1] - jolts <= 3L)) {
        paths += part2x(numbers, start+1)
    }
    if (((start + 2) < numbers.size) && (numbers[start + 2] - jolts <= 3L)) {
        paths += part2x(numbers, start+2)
    }
    if (((start + 3) < numbers.size) && (numbers[start + 3] - jolts <= 3L)) {
        paths += part2x(numbers, start+3)
    }
    return paths
}


fun part2xx(numbers: List<Long>, start: Int) : Int {
    if (start == numbers.size - 1) return 1
    if (start > numbers.size - 1) {
        println("uh oh, got start of $start out of ${numbers.size}")
        return 0
    }

//    println("starting at $start out of ${numbers.size}")
    val max = numbers.size - 2
    val jolts = numbers[start]

    var paths = 0;
    for (i in start..max) {
        if (numbers[i+1] - jolts <= 3L) {
            val x = part2x(numbers, i+1)
            paths += x
//            println("$jolts to ${numbers[i+1]} returned $x this result is now $paths")
        }
    }
//    println("starting at $start has $paths paths")
//    println("returning $result for list of size $max (${numbers[0]} - ${numbers[max]}")
    return paths
}

fun part1(numbers: ArrayList<Long>) : Int {
    val max = numbers.size - 1
    var ones = 0;
    var threes = 0;
    for (i in 1..max) {
        val diff = numbers[i] - numbers[i-1]
        println("diff $diff")
        if (diff == 1L) ones++
        else if (diff == 3L) threes++;
        else if (diff > 3L) println("hey wait... $diff")
    }

    val result = ones * threes;
    println("result $result")
    return result
}
