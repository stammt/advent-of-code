import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/dev/advent-of-code/aoc2022/input/day19sample.txt").readLines()
    day19part1(input)
}

fun day19part1(input: List<String>) {
    val blueprints = parseBlueprints(input)

    var initialState = MiningState(emptyMap(), mapOf("ore" to 1), 24)

    var qualityTotal = 0
    var count = 0
    for (i in blueprints.indices) {
        val states = mutableListOf(initialState)
        val endStates = mutableListOf<MiningState>()
        while (states.isNotEmpty()) {
            val state = states.removeAt(0)
            val nextStates = countDown(state, blueprints[i])
            for (ns in nextStates) {
                if (ns.timeRemaining == 0) {
                    endStates.add(ns)
                } else {
                    states.add(ns)
                }
            }
            count++
        }

        var geodes = -1
        for (endState in endStates) {
            if (endState.resources.containsKey("geode") && endState.resources["geode"]!! > geodes) {
                geodes = endState.resources["geode"]!!
            }
        }
        val quality = (i+1) * geodes
        qualityTotal += quality
        println("blueprint $i has $geodes (quality $quality)")
    }

    // 977 too low
    println("quality total $qualityTotal")
}

fun countDown(state: MiningState, blueprint: Blueprint): List<MiningState> {
    // what can we do with our resources?
    val nextStates = mutableListOf<MiningState>()

    // option 1: do nothing, just collect more resources
    nextStates.add(MiningState(mine(state.resources, state.robots), state.robots, state.timeRemaining - 1))

    // option 2: see what we can build
    val buildOptions = build(state, blueprint)
    val priorities = listOf("geode", "obsidian", "clay", "ore")
    for (p in priorities) {
        if (p == "geode" && state.timeRemaining < 2) continue
        if (p == "obsidian" && state.timeRemaining < 3) continue
        if (p == "clay" && state.timeRemaining < 4) continue

//        for ((type, remainingResources) in buildOptions) {
        if (buildOptions.containsKey(p)) {
            val robots = state.robots.toMutableMap()
            robots[p] = robots[p]?.plus(1) ?: 1
            nextStates.add(MiningState(mine(buildOptions[p]!!, state.robots), robots, state.timeRemaining - 1))
        }
    }

//    println("${state.timeRemaining} : ${blueprint.id} : $state produced ${nextStates.size} states: $nextStates")
    return nextStates
}

fun mine(resources: Map<String, Int>, robots: Map<String, Int>): Map<String, Int> {
    val updatedResources = mutableMapOf<String, Int>().withDefault{ _ -> 0 }
    for ((resource, count) in robots) {
        updatedResources[resource] = resources[resource]?.plus(count) ?: count
    }
    return updatedResources
}

fun build(state: MiningState, blueprint: Blueprint) : Map<String, Map<String, Int>> {
    // TODO: take time remaining and use to optimize; e.g. don't built more ore bots when only a few minutes left

    // don't create a robot if it wouldn't help because we already have the maximum yield per minute
    // e.g. the most ore we can use to build another bot is 8, so stop making ore bots if we already have 8


    // map of robot type to remaining resources after building that type
    val buildOptions = mutableMapOf<String, Map<String, Int>>()
    // try to build in order of most valuable first
    for (type in blueprint.robots.keys) {
        val shouldBuild = !state.robots.containsKey(type) || !blueprint.maxRobots.containsKey(type) || state.robots[type]!! < blueprint.maxRobots[type]!!
        if (!shouldBuild) {
            if (type != "ore") {
                println("Skipping building $type, already have ${state.robots[type]}")
            }
            continue
        }

        val robot = blueprint.robots[type]!!
        var canBuild = true
        val remainingResources = state.resources.toMutableMap()
        for ((resource, count) in robot.costs) {
            if (!state.resources.containsKey(resource)) {
                canBuild = false
                break
            }
            if (state.resources[resource]!! < count) {
                canBuild = false
                break
            }
            remainingResources[resource] = state.resources[resource]!! - count
        }
        if (canBuild) {
            buildOptions[type] = remainingResources
        }
    }

    return buildOptions
}

data class MiningState(val resources: Map<String, Int>, val robots: Map<String, Int>, val timeRemaining: Int)

data class Blueprint(val id: Int, val robots: Map<String, Robot>, val maxRobots: Map<String, Int>) {
    /**
     * ore -> clay -> obsidian -> geode
     * if we don't have a clay bot
     * >> If we can afford another ore bot:
     * >>>> would it be faster to get a clay bot by building another ore bot? If yes, do it.
     * If we have a clay bot but don't have an obsidian bot
     * >> if we can afford another ore or clay bot:
     * >>>> would it be faster to get an obsidian bot by building another ore or clay bot?
     * >> ...
     *
     * need to know at each step:
     * >> how long will it take to built a(nother) geode bot?
     * >> what bots can we afford?
     * >>>> If any, will they make it faster to build another geode bot?
     * >>>> It might be backtracking e.g. build another clay bot to build another obsidian bot faster
     * >>>> so, what bot will make it faster to build another geode bot? And then what bot would make
     * >>>> that faster, etc.
     *
     *
     */

}

data class Robot(val resource: String, val costs: Map<String, Int>) {}


fun parseBlueprints(input: List<String>) : List<Blueprint> {
    val regex = """Each (\w+) robot costs (\d+) (\w+)""".toRegex()
    val andRegex = """and (\d+) (\w+)""".toRegex()
    val blueprints = mutableListOf<Blueprint>()

    for (id in input.indices) {
        val robotDescriptions = input[id].split(": ")[1].split(". ")
        val robots = mutableMapOf<String, Robot>()
        for (r in robotDescriptions) {
            println("Parsing robot <$r>")
            val costs = mutableMapOf<String, Int>()

            val matchResult = regex.find(r)
            val (resource, cost, costResource) = matchResult!!.destructured
            costs[costResource] = cost.toInt()
            val secondCostResult = andRegex.find(r)
            if (secondCostResult != null) {
                val (cost2, costResource2) = secondCostResult!!.destructured
                costs[costResource2] = cost2.toInt()
            }

            robots[resource] = Robot(resource, costs)
        }

        // the max number of each kind of robot to make, any more than that and you
        // can't spend enough to keep up.
        val maxRobots = mutableMapOf<String, Int>()
        for ((type, robot)  in robots) {
            for ((resource, amount) in robot.costs) {
                if (type != resource && (!maxRobots.containsKey(resource) || maxRobots[resource]!! < amount)) {
                    maxRobots[resource] = amount
                }
            }
        }

        println("Parsed robots: $robots")
        println("Parsed maxRobots: $maxRobots")
        blueprints.add(Blueprint(id+1, robots, maxRobots))
    }

    return blueprints
}


