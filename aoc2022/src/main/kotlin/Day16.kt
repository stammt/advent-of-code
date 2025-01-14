import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/dev/advent-of-code/aoc2022/input/day16input.txt").readLines()
    day16part1(input)
}

data class Valve(val rate: Int, val tunnels: List<String>)

data class ValveState(val loc: String, val flow: Int, val openValves: Set<String>, val timeRemaining: Int)

var allValvesByFlowRateDescnding: List<String> = listOf()
val valveStateCache = mutableMapOf<ValveState, Int>()
var maxFlowSoFar = 0

fun day16part1(input: List<String>) {
    val valves = parseValves(input)
    val time = 30

    val initialState = ValveState("AA", 0, setOf("AA"), time)
    allValvesByFlowRateDescnding = valves.keys
        .sortedByDescending { v -> valves[v]!!.rate }

    val flow = countDown(initialState, setOf("AA"), valves)

    println("max flow: $flow")
}

fun countDown(state: ValveState, visited: Set<String>, valves: Map<String, Valve>): Int {
    if (valveStateCache.containsKey(state)) {
        return valveStateCache[state]!!
    }

    // Ran out of time
    if (state.timeRemaining == 1) {
        return state.flow
    }

    // All valves are open, just let them flow
    if (state.openValves.size == valves.size) {
        println("all valves are open with ${state.timeRemaining} left")
        return state.flow
    }

    // If we can't possibly beat the current best flow, return
    if (maxFlowSoFar > bestPotentialResult(state, valves)) {
        return 0
    }

    val v = valves[state.loc]!!
    var maxFlow = 0

    // option 1: open this valve
    if (!state.openValves.contains(state.loc)) {
        val openValves = state.openValves.toMutableSet()
        openValves.add(state.loc)
        val updatedFlow = state.flow + (v.rate * (state.timeRemaining - 1))
        val nextState = ValveState(state.loc, updatedFlow, openValves, state.timeRemaining - 1)
        maxFlow = max(maxFlow, countDown(nextState, setOf(), valves))
    }

    // option 2: go down a tunnel
    for (t in v.tunnels) {
        // don't loop around if we haven't opened a valve since the last time we were here
        if (!visited.contains(t)) {
            val nextVisited = visited.toMutableSet()
            nextVisited.add(t)
            maxFlow =
                max(maxFlow, countDown(ValveState(t, state.flow, state.openValves, state.timeRemaining - 1), nextVisited, valves))
        }

    }

    maxFlowSoFar = max(maxFlowSoFar, maxFlow)

    return maxFlow
}

// What is the best possible result from this state, assuming we could open the valves with
// the max flow within one step from each other (which probably won't happen!)
fun bestPotentialResult(state: ValveState, valves: Map<String, Valve>): Int {
    // Valves that are not open yet, sorted by flow rate descending
    val openValvesDescending = allValvesByFlowRateDescnding
        .filter { v -> !state.openValves.contains(v) }
    var bestFlow = 0
    var time = state.timeRemaining
    var nextValveIndex = 0
    while (time > 0 && nextValveIndex < openValvesDescending.size) {
        val nextValve = valves[openValvesDescending[nextValveIndex]]!!
        bestFlow += (nextValve.rate * (time - 1))
        time -= 2 // open this valve and go through a tunnel
        nextValveIndex += 1
    }
    return state.flow + bestFlow
}

fun parseValves(input: List<String>) : Map<String, Valve> {
    val valves = mutableMapOf<String, Valve>()

    for (line in input) {
        val parts = line.split(";").map { it.trim() }
        val name = parts[0].substring("Valve ".length).split(" ")[0]
        val rate = parts[0].split("=")[1].toInt()
        val tunnels = parts[1].split(", ").map { it.takeLast(2)}
        valves[name] = Valve(rate, tunnels)
    }

    return valves
}
