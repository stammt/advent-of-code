import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day16input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day16sample.txt").readLines()
    day16part2(input)
}

fun day16part2(input: List<String>) {
    val valves = parseValves(input)
    val distances = buildDistances(valves)
    val time = 30

    println("Distances $distances")
    val nonZeroValves = valves.filter { it.value.rate > 0 }

    // simple heuristic - always do the top performing valves first. Split the
    // non-zero list in half, get all combinations of each half but always do
    // the top half first.

    val nonZeroValvesSorted = nonZeroValves.values.sortedByDescending { it.rate }
//    val bestCount = nonZeroValves.size / 2
//    val worstCount = nonZeroValves.size - bestCount
    val bestCount = nonZeroValves.size -4
    val worstCount = 4
    val bestValves = nonZeroValvesSorted.take(bestCount)
    val worstValves = nonZeroValvesSorted.takeLast(worstCount)

//    println("Best: $bestValves")
//    println("Worst: $worstValves")

    println("Creating best combinations")
    val bestValvesCombinations = mutableListOf<List<String>>()
    allCombinations(listOf(), bestValves, distances, bestValvesCombinations)

    println("Creating worst combinations")
    val worstValvesCombinations = mutableListOf<List<String>>()
    allCombinations(listOf(), worstValves, distances, worstValvesCombinations)

//    println("Best combinations size: ${bestValvesCombinations}")
//    println("Worst combinations size: ${worstValvesCombinations}")

    var bestScore = 0
    var bestMePath = listOf<String>()
    var bestElephantPath = listOf<String>()
    for (best in bestValvesCombinations) {
        for (worst in worstValvesCombinations) {
            val path = best + worst

            // alternate valves for me and the elephant
            val mePath = mutableListOf<String>("AA")
            val elephantPath = mutableListOf<String>("AA")
            var i = 0
            do {
                mePath += path[i]
                i++
                if (i < path.size) {
                    elephantPath += path[i]
                    i++
                }
            } while (i < path.size)


            val total = scoreForTwo(mePath, elephantPath, valves, distances)
            println("$total for me $mePath and elephant $elephantPath")

            if (total > bestScore) {
                bestScore = total
                bestMePath = mePath
                bestElephantPath = elephantPath
            }
        }
    }

    // 2963 is too low
    println("Part 2 total: $bestScore for $bestMePath and $bestElephantPath")
}


fun day16part1(input: List<String>) {
    val valves = parseValves(input)
    val distances = buildDistances(valves)
    val time = 30

    println("Distances $distances")
    val nonZeroValves = valves.filter { it.value.rate > 0 }
    val result = mutableListOf<Int>()

    // simple heuristic - always do the top performing valves first. Split the
    // non-zero list in half, get all combinations of each half but always do
    // the top half first.

    val nonZeroValvesSorted = nonZeroValves.values.sortedByDescending { it.rate }
//    val bestCount = nonZeroValves.size / 2
//    val worstCount = nonZeroValves.size - bestCount
    val bestCount = nonZeroValves.size -5
    val worstCount = 5
    val bestValves = nonZeroValvesSorted.take(bestCount)
    val worstValves = nonZeroValvesSorted.takeLast(worstCount)

    println("Best: $bestValves")
    println("Worst: $worstValves")

    val bestValvesCombinations = mutableListOf<List<String>>()
    allCombinations(listOf("AA"), bestValves, distances, bestValvesCombinations)
    val worstValvesCombinations = mutableListOf<List<String>>()
    allCombinations(listOf(), worstValves, distances, worstValvesCombinations)

    println("Best combinations size: ${bestValvesCombinations}")
    println("Worst combinations size: ${worstValvesCombinations}")

    var bestScore = 0
    var bestPath = listOf<String>()
    for (best in bestValvesCombinations) {
        for (worst in worstValvesCombinations) {
            val path = best + worst
            val total = score(path, valves, distances)

            if (total > bestScore) {
                bestScore = total
                bestPath = path
            }
        }
    }

    println("Part 1 total: $bestScore for $bestPath")
}

fun score(path: List<String>, valves: Map<String, Valve>, distances: Map<Pair<String, String>, List<String>>) : Int {
    val time = 30
    var minute = 0
    var flow = 0
    var total = 0
    for (i in 1 until path.size) {
        val distance = distances[path[i-1] to path[i]]!!.size
        val steps = min((distance + 1), time - minute)
        minute += steps
        total += (flow * steps)
        flow += valves[path[i]]!!.rate
    }
    if (minute < time) {
        total += ((time - minute) * flow)
    }

    return total
}

fun scoreForTwo(mePath: List<String>, elephantPath: List<String>, valves: Map<String, Valve>, distances: Map<Pair<String, String>, List<String>>) : Int {
    val time = 26
//    var minute = 1
    var flow = 0
    var total = 0

    // where we are in the path
    var mePathIndex = 1
    var elephantPathIndex = 1

    // minutes left until we reach the next valve and open it
    var meStepTimeRemaining = distances["AA" to mePath[mePathIndex]]!!.size
    var elephantStepTimeRemaining = distances["AA" to elephantPath[elephantPathIndex]]!!.size

    for (minute in 1..time) {
//        println("Minute $minute flow is $flow")
        total += flow

        if (meStepTimeRemaining == 0) {
            if (mePathIndex < mePath.size) {
                val meValve = mePath[mePathIndex]!!
//                println("Me opening valve $meValve")
                flow += valves[meValve]!!.rate
                mePathIndex++
                if (mePathIndex < mePath.size) {
                    meStepTimeRemaining = distances[meValve to mePath[mePathIndex]]!!.size
                }
            }
        } else {
            meStepTimeRemaining--
        }
//        meStepTimeRemaining = max(0, meStepTimeRemaining - 1)

        if (elephantStepTimeRemaining == 0) {
            if (elephantPathIndex < elephantPath.size) {
                val elephantValve = elephantPath[elephantPathIndex]!!
//                println("Elephant opening valve $elephantValve")
                flow += valves[elephantValve]!!.rate
                elephantPathIndex++
                if (elephantPathIndex < elephantPath.size) {
                    elephantStepTimeRemaining =
                        distances[elephantValve to elephantPath[elephantPathIndex]]!!.size
                }
            }
        } else {
            elephantStepTimeRemaining--
        }
//        elephantStepTimeRemaining = max(0, elephantStepTimeRemaining - 1)

//        println("After minute $minute: total $total, flow $flow : $mePathIndex ($meStepTimeRemaining) $elephantPathIndex ($elephantStepTimeRemaining)")
    }

    return total
}


fun allCombinations(path: List<String>, valves: List<Valve>, distances: Map<Pair<String, String>, List<String>>, results: MutableList<List<String>>) {
    val remaining = valves.toMutableList()
    remaining.removeIf { path.contains(it.name) }

    if (remaining.isEmpty()) {
        results.add(path)
    } else {
        for (valve in remaining) {
            val appended = path.toMutableList()
            appended.add(valve.name)
            allCombinations(appended, valves, distances, results)
        }
    }
}



fun getNextBestValve(current: String, time: Int, openValves: Set<String>, valves: Map<String, Valve>, distances: Map<Pair<String, String>, List<String>>) : List<String> {
    val closedValves = valves.filter { it.value.rate > 0 && !openValves.contains(it.key) }
    var bestScore = 0
    var bestValve = listOf<String>()
    for (valve in closedValves) {
        val distance = distances[current to valve.key]!!
        val score = (time - distance.size - 1) * valve.value.rate
//        println("checking $current to ${valve.key} : $score from $distance at $time")
        if (score > bestScore) {
            bestScore = score
            bestValve = distance
        }
    }
//    println("Best valve from $current is $bestValve")
    return bestValve
}

data class ValveResult(var result: Int) {
    fun recordTotal(total: Int) {
        result = max(result, total)
    }
}

fun buildPaths(path: List<String>,
               total: Int,
               time: Int,
               flowPerMinute: Int,
               valves: Map<String, Valve>,
               distances: Map<Pair<String, String>, List<String>>,
               totals: MutableList<Int>) {
    if (time == 0) {
//        println("Adding total $total for $path")
        totals.add(total)
    } else if (path.containsAll(valves.keys)) {
        buildPaths(path, total + flowPerMinute, time - 1, flowPerMinute, valves, distances, totals)
    } else {
        for (node in valves) {
            if (!path.contains(node.key)) {
                val moveTime = distances[path.last() to node.key]!!.size

                // If we'll take too long, cap it at the remaining time. Otherwise add 1 for opening the valve.
                val elapsedTime = if (moveTime < time) moveTime + 1 else time

//                println("Elapsed time from $path to ${node.key} is $elapsedTime")
                buildPaths(path + node.key, total + (flowPerMinute * elapsedTime), time - elapsedTime,
                    flowPerMinute + node.value.rate,
                                valves, distances, totals)
            }
        }
    }
}

// figure out the distances between each non-zero valve, and from AA to all non-zero valves
fun buildDistances(valves: Map<String, Valve>) : Map<Pair<String, String>, List<String>> {
    val paths = mutableMapOf<Pair<String, String>, List<String>>()
    for (valve in valves) {
        val d = dijkstra(valve.key, valves)
        for (key in d.keys) {
            paths[key] = d[key]!!
        }
    }
    return paths
}

fun dijkstra(start: String, valves: Map<String, Valve>) : Map<Pair<String, String>, List<String>> {
    val distances = mutableMapOf<String, Int>()
    val prev = mutableMapOf<String, String>()
    val q = valves.keys.toMutableList()
    distances[start] = 0

    do {
        val u = q.minBy { if (!distances.containsKey(it)) Int.MAX_VALUE else distances[it]!! }
        q.remove(u)
        val uValve = valves[u]!!
        for (neighbor in uValve.tunnels) {
            val alt = distances[u]!! + 1
            if (!distances.containsKey(neighbor) || alt < distances[neighbor]!!) {
                distances[neighbor] = alt
                prev[neighbor] = u
            }
        }
    } while (q.isNotEmpty())

    val paths = mutableMapOf<Pair<String, String>, List<String>>()
    for (valve in valves) {
        if (valve.key != start) {
            val path = mutableListOf<String>(valve.key)
            var v = valve.key
            while (prev.containsKey(v) && prev[v] != start) {
                path.add(0, prev[v]!!)
                v = prev[v]!!
            }
            paths[start to valve.key] = path
        }
    }
    return paths
}



data class Valve(val name: String, val rate: Int, val tunnels: List<String>) {
//    var open = false
}

fun eligibleValvesRemaining(openValves: Set<String>, valves: Map<String, Valve>) : Boolean {
    return valves.filter { !openValves.contains(it.key) && it.value.rate > 0 }.isNotEmpty()
}


fun parseValves(input: List<String>) : Map<String, Valve> {
    val valves = mutableMapOf<String, Valve>()

    for (line in input) {
        val parts = line.split(";").map { it.trim() }
        val name = parts[0].substring("Valve ".length).split(" ")[0]
        val rate = parts[0].split("=")[1].toInt()
        val tunnels = parts[1].split(", ").map { it.takeLast(2)}
        valves[name] = Valve(name, rate, tunnels)
    }

    println("Parsed valves:")
    for (v in valves) {
        println(v)
    }

    return valves
}
