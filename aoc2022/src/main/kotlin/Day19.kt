import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/dev/advent-of-code/aoc2022/input/day19input.txt").readLines()
    day19part1(input)
}

var stateCacheHits = 0

fun day19part2(input: List<String>) {
    val blueprints = parseBlueprints(input)

    val initialState = MiningState(Resources(0, 0, 0, 0),
        Resources(1, 0, 0, 0),
        Resources(0, 0, 0, 0),
        32)

    var result = 0
    for (i in 0..2) {
        stateCache.clear()
        maxResult = 0

        val endState = countDown(initialState, blueprints[i])

        println("\nblueprint ${i+1} has ${endState}\n")
        result = if (result == 0) endState else (result * endState)
    }
    // 33, 10, 25 = 8250
    println("result total $result")
}


fun day19part1(input: List<String>) {
    val blueprints = parseBlueprints(input)

    val initialState = MiningState(Resources(0, 0, 0, 0),
        Resources(1, 0, 0, 0),
        Resources(0, 0, 0, 0),
        24)

    var qualityTotal = 0
    for (i in blueprints.indices) {
        stateCache.clear()
        maxResult = 0

        val endState = countDown(initialState, blueprints[i])

        val quality = (i + 1) * endState
        qualityTotal += quality
        println("\nblueprint ${i+1} has ${endState} (quality $quality)\n")
    }

    println("quality total $qualityTotal")
}

val stateCache = mutableMapOf<MiningState, Int>()
val buildAnything = Resources(0, 0, 0, 0)
var maxResult = 0

fun countDown(state: MiningState, blueprint: Blueprint): Int {
//    println("time remaining ${state.timeRemaining}")
    if (stateCache.containsKey(state)) {
//        println("*** state cache hit for $state")
        stateCacheHits++
        return stateCache[state]!!
    }
    if (state.timeRemaining == 1) {
        // Last minute, just mine, no more robots
        val result = state.resources.add(state.robots).geode
        maxResult = max(result, maxResult)
        return result
    }

    // It's hopeless :(
    if (!canBeatResult(maxResult, state)) {
        return 0
    }

    // what can we do with our resources?
    var result = -1

    // option 2: see what we can build, prioritizing geode robots
    if (state.resources.canBuild(blueprint.geodeRobot)) {
        val nextResources = state.resources.remove(blueprint.geodeRobot).add(state.robots)
        result  = max(result, countDown(MiningState(nextResources,
            state.robots.add(0, 0, 0, 1),
            buildAnything,
            state.timeRemaining - 1), blueprint))
    } else {
        var canBuildObsidian = 0
        if (state.canBuild.obsidian == 0 && state.robots.obsidian < blueprint.maxRobots.obsidian && state.resources.canBuild(blueprint.obsidianRobot)) {
            canBuildObsidian = 1
            val nextResources = state.resources.remove(blueprint.obsidianRobot).add(state.robots)
            result = max(result, countDown(MiningState(nextResources,
                state.robots.add(0, 0, 1, 0),
                buildAnything,
                state.timeRemaining - 1), blueprint))
        }
        var canBuildClay = 0
        if (state.canBuild.clay == 0 && state.robots.clay < blueprint.maxRobots.clay && state.resources.canBuild(blueprint.clayRobot)) {
            canBuildClay = 1
            val nextResources = state.resources.remove(blueprint.clayRobot).add(state.robots)
            result = max(result, countDown(MiningState(nextResources,
                state.robots.add(0, 1, 0, 0),
                buildAnything,
                state.timeRemaining - 1), blueprint))
        }
        var canBuildOre = 0
        if (state.canBuild.ore == 0 && state.robots.ore < blueprint.maxRobots.ore && state.resources.canBuild(blueprint.oreRobot)) {
            canBuildOre = 1
            val nextResources = state.resources.remove(blueprint.oreRobot).add(state.robots)
            result = max(result, countDown(MiningState(nextResources,
                state.robots.add(1, 0, 0, 0),
                buildAnything,
                state.timeRemaining - 1), blueprint))
        }

        // do nothing, just collect more resources
        result = max(result, countDown(MiningState(state.resources.add(state.robots), state.robots,
            Resources(canBuildOre, canBuildClay, canBuildObsidian, 0),
            state.timeRemaining - 1), blueprint))

    }

    stateCache[state] = result
//    println("${state.timeRemaining} : ${blueprint.id} : $state produced ${nextStates.size} states: $nextStates")
    return result
}

// Is it possible to beat this result?
fun canBeatResult(result: Int, state: MiningState): Boolean {
    return state.resources.geode + maxFutureGeodes(state) >= result
}

// Max number of geodes we could mine even if we build a new geode bot every turn
fun maxFutureGeodes(state: MiningState): Int {
    return (state.timeRemaining * state.robots.geode) + (state.timeRemaining * ((state.timeRemaining - 1) / 2))
}

data class MiningState(val resources: Resources, // Current resources
                       val robots: Resources, // Current robots per resource
                       val canBuild: Resources, // Track what could have been built but was skipped, so we don't just do it later to get the same result
                       val timeRemaining: Int)

data class Resources(val ore: Int, val clay: Int, val obsidian: Int, val geode: Int) {
    fun add(other: Resources): Resources {
        return Resources(ore + other.ore, clay + other.clay, obsidian + other.obsidian, geode + other.geode)
    }

    fun add(ore1: Int, clay1: Int, obsidian1: Int, geode1: Int): Resources {
        return Resources(ore + ore1, clay + clay1, obsidian + obsidian1, geode + geode1)
    }

    fun remove(other: Resources): Resources {
        return Resources(ore - other.ore, clay - other.clay, obsidian - other.obsidian, geode - other.geode)
    }

    fun canBuild(robot: Resources): Boolean {
        return robot.ore <= ore
                && robot.clay <= clay
                && robot.obsidian <= obsidian
                && robot.geode <= geode
    }

    fun times(t: Int): Resources {
        return Resources(ore * t, clay * t, obsidian * t, geode * t)
    }
}

data class Blueprint(
    val id: Int,
    val oreRobot: Resources,
    val clayRobot: Resources,
    val obsidianRobot: Resources,
    val geodeRobot: Resources,
    val maxRobots: Resources
)

fun parseBlueprints(input: List<String>): List<Blueprint> {
    val regex = """Each (\w+) robot costs (\d+) (\w+)""".toRegex()
    val andRegex = """and (\d+) (\w+)""".toRegex()
    val blueprints = mutableListOf<Blueprint>()

    for (id in input.indices) {
        val robotDescriptions = input[id].split(": ")[1].split(". ")
        var oreRobot: Resources? = null
        var clayRobot: Resources? = null
        var obsidianRobot: Resources? = null
        var geodeRobot: Resources? = null

        var maxOre = 0
        var maxClay = 0
        var maxObsidian = 0
        var maxGeode = Int.MAX_VALUE
        for (r in robotDescriptions) {
            println("Parsing robot <$r>")
            var ore = 0
            var clay = 0
            var obsidian = 0
            var geode = 0

            val matchResult = regex.find(r)
            val (resource, cost, costResource) = matchResult!!.destructured
            when (costResource) {
                "ore" -> ore = cost.toInt()
                "clay" -> clay = cost.toInt()
                "obsidian" -> obsidian = cost.toInt()
                "geode" -> geode = cost.toInt()
            }

            val secondCostResult = andRegex.find(r)
            if (secondCostResult != null) {
                val (cost2, costResource2) = secondCostResult!!.destructured
                when (costResource2) {
                    "ore" -> ore += cost2.toInt()
                    "clay" -> clay += cost2.toInt()
                    "obsidian" -> obsidian += cost2.toInt()
                    "geode" -> geode += cost2.toInt()
                }
            }
            val robotCost = Resources(ore, clay, obsidian, geode)
            when (resource) {
                "ore" -> oreRobot = robotCost
                "clay" -> clayRobot = robotCost
                "obsidian" -> obsidianRobot = robotCost
                "geode" -> geodeRobot = robotCost
            }
            maxOre = max(maxOre, robotCost.ore)
            maxClay = max(maxClay, robotCost.clay)
            maxObsidian = max(maxObsidian, robotCost.obsidian)
        }

        // the max number of each kind of robot to make, any more than that and you
        // can't spend enough to keep up.
        val maxRobots = Resources(maxOre, maxClay, maxObsidian, maxGeode)
        val bp = Blueprint(id+1, oreRobot!!, clayRobot!!, obsidianRobot!!, geodeRobot!!, maxRobots)
        println("Parsed robots: $bp")
        blueprints.add(bp)
    }

    return blueprints
}


