import java.io.File

fun main(args: Array<String>) {
    val lines = File("/Users/stammt/dev/aoc/day9input.txt").readLines()
    val numbers = ArrayList<Long>()
    lines.forEach {
        numbers.add(it.toLong())
    }

//    partOne(numbers)

    /*
    found range 396 .. 412 , sum 3353494,  min 1140297 max 2213197
result 3353494
     */
    val targetIndex = 508;
    val result = partTwoBruteForce(numbers, targetIndex)
    println("result $result")
}

fun partTwoBruteForce(numbers: List<Long>, targetIndex: Int) : Long {
    val targetValue = numbers[targetIndex]
    var start = 0;

    do {
        var end = start + 1;
        var sum = numbers[start]

        do {
            sum += numbers[end];
            println("checking $start .. $end ($sum) against $targetValue")
            if (sum == targetValue) return smallestPlusLargest(numbers, start, end)
        } while (++end < targetIndex && sum <= targetValue)

    } while (++start < targetIndex - 1)

    return -1
}

fun smallestPlusLargest(numbers: List<Long>, start: Int, end: Int) : Long {
    val range = numbers.subList(start, end + 1)
    val min = range.minOrNull()
    val max = range.maxOrNull()
    var sum = 0L
    if (min != null) {
        sum = min+ max!!
    }
    return sum
}

fun partOne(numbers: List<Long>) {
    var i = 25;
    var firstInvalid = -1;
    while (i < numbers.size) {
        val validSums = sums(numbers.subList(i - 25, i))
        val isValid = validSums.contains(numbers[i])
        println("checking $i: ${numbers[i]} $isValid")
        if (!isValid && firstInvalid == -1) {
            firstInvalid = i;
        }
        i++;
    }

    println("first invalid is ${numbers[firstInvalid]} at index $firstInvalid")
}

fun sums(preamble: List<Long>) : Set<Long> {
    val values = HashSet<Long>()
    val max = preamble.size - 1
    for (i in 0..max) {
        for (j in i..max) {
            if (preamble[i] != preamble[j]) {
                values.add(preamble[i] + preamble[j])
            }
        }
    }
    return values
}

