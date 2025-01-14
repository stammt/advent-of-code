import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/dev/advent-of-code/aoc2022/input/day16input.txt").readLines()
    day16part2(input)
}

data class Valve(val rate: Int, val tunnels: List<String>)

data class ValveState(val loc: String, val elephant: String, val flow: Int, val openValves: Set<String>, val timeRemaining: Int)

var allValvesByFlowRateDescnding: List<String> = listOf()
val valveStateCache = mutableMapOf<ValveState, Int>()
var maxFlowSoFar = 0

fun day16part1(input: List<String>) {
    val valves = parseValves(input)
    val time = 30

    val initialState = ValveState("AA", "",0, setOf("AA"), time)
    allValvesByFlowRateDescnding = valves.keys
        .sortedByDescending { v -> valves[v]!!.rate }

    val flow = countDown(initialState, setOf("AA"), valves)

    println("max flow: $flow")
}

fun day16part2(input: List<String>) {
    val valves = parseValves(input)
    val time = 26

    val initialState = ValveState("AA", "AA",0, setOf("AA"), time)
    allValvesByFlowRateDescnding = valves.keys
        .sortedByDescending { v -> valves[v]!!.rate }

    val (flow, choices) = countDownWithElephant(initialState, setOf("AA"), setOf("AA"), valves)

    for (c in choices.reversed()) {
        println(c)
        println()
    }
    println("max flow with elephant: $flow")
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
        val nextState = ValveState(state.loc, "", updatedFlow, openValves, state.timeRemaining - 1)
        maxFlow = max(maxFlow, countDown(nextState, setOf(), valves))
    }

    // option 2: go down a tunnel
    for (t in v.tunnels) {
        // don't loop around if we haven't opened a valve since the last time we were here
        if (!visited.contains(t)) {
            val nextVisited = visited.toMutableSet()
            nextVisited.add(t)
            maxFlow =
                max(maxFlow, countDown(ValveState(t, "", state.flow, state.openValves, state.timeRemaining - 1), nextVisited, valves))
        }
    }

    maxFlowSoFar = max(maxFlowSoFar, maxFlow)
    return maxFlow
}

fun countDownWithElephant(state: ValveState,
                          visited: Set<String>,
                          elephantVisited: Set<String>,
                          valves: Map<String, Valve>): Pair<Int, List<String>> {
    if (valveStateCache.containsKey(state)) {
        println("*** cache hit $state")
        return valveStateCache[state]!! to listOf("Cache hit: $state")
    }

    // Ran out of time
    if (state.timeRemaining == 1) {
        return state.flow to listOf("Out of time: $state")
    }

    // All valves are open, just let them flow
    if (state.openValves.size == valves.size) {
        return state.flow to listOf("All valves open: $state")
    }

    // If we can't possibly beat the current best flow, return
    if (maxFlowSoFar > bestPotentialResultWithElephant(state, valves)) {
        if (state.timeRemaining == 26) {
            println("$state - cutting off, max $maxFlowSoFar > ${bestPotentialResultWithElephant(state, valves)}")
        }
        return 0 to listOf("$state Stopping, max $maxFlowSoFar > ${bestPotentialResultWithElephant(state, valves)}")
    }

    val myValve = valves[state.loc]!!
    val elephantValve = valves[state.elephant]!!
    var maxFlow = 0
    var maxChoices = mutableListOf<String>()

    // Call recursively with each combination of me + elephant opening valves
    // and following tunnels
    // If me and elephant are at the same valve, only open it once
    // Don't let either of us loop without opening a valve (track separate visited?)

    // me and elephant both open valves
    if (!state.openValves.contains(state.loc) && !state.openValves.contains(state.elephant) && state.loc != state.elephant) {
        val openValves = state.openValves.toMutableSet()
        openValves.add(state.loc)
        openValves.add(state.elephant)
        val updatedFlow = state.flow + (myValve.rate * (state.timeRemaining - 1)) + (elephantValve.rate * (state.timeRemaining - 1))
        val nextState = ValveState(state.loc, state.elephant, updatedFlow, openValves, state.timeRemaining - 1)

        val (flow, choices) =  countDownWithElephant(nextState, setOf(), setOf(), valves)
        if (flow > maxFlow) {
            maxFlow = flow
            maxChoices = choices.toMutableList()
            maxChoices.add("$state Both opening valves, I open ${state.loc} he opens ${state.elephant}, flow goes from ${state.flow} to $updatedFlow")
        }
    }

    if (!state.openValves.contains(state.loc)) {
        // I open a valve, the elephant walks
        val openValves = state.openValves.toMutableSet()
        openValves.add(state.loc)
        val updatedFlow = state.flow + (myValve.rate * (state.timeRemaining - 1))

        var walked = false
        for (t in elephantValve.tunnels) {
            if (!elephantVisited.contains(t)) {
                walked = true
                val nextVisited = elephantVisited.toMutableSet()
                nextVisited.add(t)
                val nextState = ValveState(state.loc, t, updatedFlow, openValves, state.timeRemaining - 1)
                val (flow, choices) = countDownWithElephant(nextState, setOf(), nextVisited, valves)
                if (flow > maxFlow) {
                    maxFlow = flow
                    maxChoices = choices.toMutableList()
                    maxChoices.add("$state I open ${state.loc} he goes from ${state.elephant} to ${t}, flow goes from ${state.flow} to $updatedFlow")
                }
            }
        }
        // If the elephant didn't have anywhere to go, make sure my valve gets opened
        if (!walked) {
            val nextState = ValveState(state.loc, state.elephant, updatedFlow, openValves, state.timeRemaining - 1)
            val (flow, choices) = countDownWithElephant(nextState, setOf(), elephantVisited, valves)
            if (flow > maxFlow) {
                maxFlow = flow
                maxChoices = choices.toMutableList()
                maxChoices.add("$state I opened ${state.loc}, he didn't have anywhere to go. flow goes from ${state.flow} to $updatedFlow")
            }
        }
    }
    if (!state.openValves.contains(state.elephant)) {
        // Elephant opens a valve, I walk
        val openValves = state.openValves.toMutableSet()
        openValves.add(state.elephant)
        val updatedFlow = state.flow + (elephantValve.rate * (state.timeRemaining - 1))

        var walked = false
        for (t in myValve.tunnels) {
            if (!visited.contains(t)) {
//                println("${state.timeRemaining}: he open ${state.elephant} I go to ${t}, flow goes from ${state.flow} to $updatedFlow")
                walked = true
                val nextVisited = visited.toMutableSet()
                nextVisited.add(t)
                val nextState = ValveState(t, state.elephant, updatedFlow, openValves, state.timeRemaining - 1)
                val (flow, choices) = countDownWithElephant(nextState, nextVisited, setOf(), valves)
                if (flow > maxFlow) {
                    maxFlow = flow
                    maxChoices = choices.toMutableList()
                    maxChoices.add("$state He opened ${state.elephant}, I went from ${state.loc} to $t. flow goes from ${state.flow} to $updatedFlow")
                }
            }
        }
        // If I didn't have anywhere to go, make sure my valve gets opened
        if (!walked) {
            val nextState = ValveState(state.loc, state.elephant, updatedFlow, openValves, state.timeRemaining - 1)
            val (flow, choices) = countDownWithElephant(nextState, visited, setOf(), valves)
            if (flow > maxFlow) {
                maxFlow = flow
                maxChoices = choices.toMutableList()
                maxChoices.add("$state He opened ${state.elephant}, I didn't have anywhere to go. flow goes from ${state.flow} to $updatedFlow")
            }
        }
    }

    // We both walk. See what tunnels have not been visited
    val myTunnels = myValve.tunnels.filter { t -> !visited.contains(t) }
    val elephantTunnels = elephantValve.tunnels.filter {t -> !elephantVisited.contains(t) }

    if (myTunnels.isNotEmpty() && elephantTunnels.isNotEmpty()) {
        for (myTunnel in myTunnels) {
            for (elephantTunnel in elephantTunnels) {
                val nextVisited = visited.toMutableSet()
                nextVisited.add(myTunnel)
                val nextElephantVisited = elephantVisited.toMutableSet()
                nextElephantVisited.add(elephantTunnel)
                val (flow, choices) =
                    countDownWithElephant(ValveState(myTunnel,
                        elephantTunnel,
                        state.flow,
                        state.openValves,
                        state.timeRemaining - 1),
                        nextVisited,
                        nextElephantVisited,
                        valves)
                // right answer check
                if (state.timeRemaining == 26 && state.loc == "AA" && myTunnel == "II" && state.elephant == "AA" && elephantTunnel == "DD") {
                    println("Answer check: flow is $flow max is $maxFlow - $state ")
                }
                if (flow > maxFlow) {
                    maxFlow = flow
                    maxChoices = choices.toMutableList()
                    maxChoices.add("$state Both walking - I go from ${state.loc} to ${myTunnel} he goes from ${state.elephant} to ${elephantTunnel}")
                }
            }
        }
    } else if (myTunnels.isNotEmpty()) {
        for (myTunnel in myTunnels) {
            val nextVisited = visited.toMutableSet()
            nextVisited.add(myTunnel)
            val (flow, choices) =
                countDownWithElephant(ValveState(myTunnel,
                    state.elephant,
                    state.flow,
                    state.openValves,
                    state.timeRemaining - 1),
                    nextVisited,
                    elephantVisited,
                    valves)
            if (flow > maxFlow) {
                maxFlow = flow
                maxChoices = choices.toMutableList()
                maxChoices.add("$state I go from ${state.loc} to ${myTunnel} he stays at ${state.elephant}")
            }
        }
    } else if (elephantTunnels.isNotEmpty()) {
        for (elephantTunnel in elephantTunnels) {
            val nextElephantVisited = elephantVisited.toMutableSet()
            nextElephantVisited.add(elephantTunnel)
            val (flow, choices) =
                countDownWithElephant(ValveState(state.loc,
                    elephantTunnel,
                    state.flow,
                    state.openValves,
                    state.timeRemaining - 1),
                    visited,
                    nextElephantVisited,
                    valves)
            if (flow > maxFlow) {
                maxFlow = flow
                maxChoices = choices.toMutableList()
                maxChoices.add("$state He goes from ${state.elephant} to ${elephantTunnel} I stay at ${state.loc}")
            }
        }
    }

    maxFlowSoFar = max(maxFlowSoFar, maxFlow)

    return maxFlow to maxChoices
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

// What is the best possible result from this state, assuming we could open the valves with
// the max flow within one step from each other (which probably won't happen!)
fun bestPotentialResultWithElephant(state: ValveState, valves: Map<String, Valve>): Int {
    // Valves that are not open yet, sorted by flow rate descending
    val openValvesDescending = allValvesByFlowRateDescnding
        .filter { v -> !state.openValves.contains(v) }
    var bestFlow = 0
    var time = state.timeRemaining
    var nextValveIndex = 0
    while (time > 0 && nextValveIndex < openValvesDescending.size) {
        var nextValve = valves[openValvesDescending[nextValveIndex]]!!
        bestFlow += (nextValve.rate * (time - 1))
        nextValveIndex += 1
        // elephant opens a valve too
        if (nextValveIndex < openValvesDescending.size) {
            nextValve = valves[openValvesDescending[nextValveIndex]]!!
            bestFlow += (nextValve.rate * (time - 1))
            nextValveIndex += 1
        }
        time -= 3 // open this valve and go through a tunnel
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
