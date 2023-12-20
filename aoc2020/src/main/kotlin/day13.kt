import java.io.File
import java.lang.Math.floor
import java.time.Duration
import java.time.Instant
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day13input.txt").readLines()

    day13Part2(input)
}

fun day13Part2(input : List<String>) {
    val buses = input[1].trim().split(",")

    // pair of id, offset
    val values = mutableListOf<Long>()
    val mods = mutableListOf<Long>()
    for (i in buses.indices) {
        if (buses[i] != "x") {
            val id = buses[i].toLong()
            values.add(id)
            mods.add(id - i.toLong())
        }
    }
    val result = chineseRemainder(values.toLongArray(), mods.toLongArray())
    println("result: $result")
}

fun day13Part2x(input : List<String>) {
    val buses = input[1].trim().split(",")

    // pair of id, offset
    val offsets = mutableListOf<Pair<Long, Int>>()
    var maxId = -1L
    var maxIdIndex = -1
    for(i in buses.indices) {
        if (buses[i] != "x") {
            val id = buses[i].toLong()
            if (id > maxId) {
                maxId = id
                maxIdIndex = i
            }
            offsets.add(Pair(id, i))
        }
    }

    offsets.sortByDescending { it.first }

    val firstId = offsets[0].first // buses[0].toLong()
    val firstOffset = offsets[0].second

    val mod = 100000000000000L % firstId
    //          more than 71464099999983
//
    var depart =  100000000000000L - mod - firstOffset
//    var depart = firstId - firstOffset
    println("double check should be zero: ${(depart + firstOffset) % firstId}")

//    var multiplier = (maxId - maxIdIndex) / firstId
//    println(" multiplier between $firstId and $maxId - $maxIdIndex is $multiplier")

    var found = false
    var count = 0L;
    var highestCheck = 0
    while (!found) {
        count++
        var check = 0
        while (check < offsets.size) {
            val x = depart + offsets[check].first + offsets[check].second
            if ((x % offsets[check].first) != 0L) {
                break
            }
            check++
        }
        if (check == offsets.size) {
            println("found!")
            found = true
        } else if (check > highestCheck) {
            highestCheck = check
            println(" new highest check $highestCheck out of ${offsets.size}")
        } else if (count % 100000000L == 0L) {
           println("still looking, $count $depart ($check) ($highestCheck) ")
        }

        if (!found) {
            depart += (firstId)
        }
    }

    if (found) {
        println("Found $depart")
    } else {
        println("not found!")
    }

}


/* returns x where (a * x) % b == 1 */
fun multInv(a: Long, b: Long): Long {
    if (b == 1L) return 1
    var aa = a
    var bb = b
    var x0 = 0L
    var x1 = 1L
    while (aa > 1) {
        val q = aa / bb
        var t = bb
        bb = aa % bb
        aa = t
        t = x0
        x0 = x1 - q * x0
        x1 = t
    }
    if (x1 < 0) x1 += b
    return x1
}

fun chineseRemainder(n: LongArray, a: LongArray): Long {
    val prod: Long = n.fold(1) { acc, i -> acc * i }
    var sum = 0L
    for (i in 0 until n.size) {
        val p: Long = prod / n[i]
        sum += a[i] * multInv(p, n[i]) * p
    }
    return sum % prod
}

fun day13Part1(input : List<String>) {
    var arrival = input[0].trim().toInt()
    var buses = input[1].trim().split(",")

//    val minutesToWait = mutableMapOf<Int, Int>()
    var bestId = -1
    var bestMinutesToWait = Int.MAX_VALUE
    buses.forEach {
        if (it.trim() != "x") {
            val id = it.toInt();
            var depart = 0;
            while (depart <= arrival) {
                depart += id
            }
            val minutes = (depart - arrival)
//            minutesToWait[id] = minutes
            if (minutes < bestMinutesToWait) {
                bestId = id
                bestMinutesToWait = minutes
            }
        }
    }

    val result = bestId * bestMinutesToWait
    print("$result for $bestId .. $bestMinutesToWait")

}

