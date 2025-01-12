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
fun day19part1(input: List<String>) {
    val blueprints = parseBlueprints(input)

    val initialState = MiningState(Resources(0, 0, 0, 0),
        Resources(1, 0, 0, 0),
        24)

    var qualityTotal = 0
    var count = 0
    for (i in blueprints.indices) {
        stateCache.clear()
        count = 0

        val endState = countDown(initialState, blueprints[i])

        val quality = (i + 1) * endState.resources.geode
        qualityTotal += quality
        println("\nblueprint ${i+1} has ${endState.resources.geode} (quality $quality)\n")
    }

    // 977 too low
    println("quality total $qualityTotal")
}

val stateCache = mutableMapOf<Pair<MiningState, Blueprint>, MiningState>()
fun countDown(state: MiningState, blueprint: Blueprint): MiningState {
//    println("time remaining ${state.timeRemaining}")
    if (stateCache.containsKey(state to blueprint)) {
//        println("*** state cache hit for $state")
        stateCacheHits++
        return stateCache[state to blueprint]!!
    }
    // what can we do with our resources?
    val nextStates = mutableListOf<MiningState>()

    // option 1: do nothing, just collect more resources
    nextStates.add(MiningState(state.resources.add(state.robots), state.robots, state.timeRemaining - 1))

    // option 2: see what we can build
    if (state.robots.ore < blueprint.maxRobots.ore && state.resources.canBuild(blueprint.oreRobot)) {
        val nextResources = state.resources.remove(blueprint.oreRobot).add(state.robots)
        nextStates.add(MiningState(nextResources,
            state.robots.add(Resources(1, 0, 0, 0)),
            state.timeRemaining - 1))
    }
    if (state.robots.clay < blueprint.maxRobots.clay && state.resources.canBuild(blueprint.clayRobot)) {
        val nextResources = state.resources.remove(blueprint.clayRobot).add(state.robots)
        nextStates.add(MiningState(nextResources,
            state.robots.add(Resources(0, 1, 0, 0)),
            state.timeRemaining - 1))
    }
    if (state.robots.obsidian < blueprint.maxRobots.obsidian && state.resources.canBuild(blueprint.obsidianRobot)) {
        val nextResources = state.resources.remove(blueprint.obsidianRobot).add(state.robots)
        nextStates.add(MiningState(nextResources,
            state.robots.add(Resources(0, 0, 1, 0)),
            state.timeRemaining - 1))
    }
    if (state.resources.canBuild(blueprint.geodeRobot)) {
        val nextResources = state.resources.remove(blueprint.geodeRobot).add(state.robots)
        nextStates.add(MiningState(nextResources,
            state.robots.add(Resources(0, 0, 0, 1)),
            state.timeRemaining - 1))
    }

    if (state.timeRemaining == 1) {
        return maxGeodes(nextStates)
    }

    val endStates = mutableListOf<MiningState>()
    for (branch in nextStates) {
        endStates.add(countDown(branch, blueprint))
    }
    val result = maxGeodes(endStates)

    stateCache[state to blueprint] = result
//    println("${state.timeRemaining} : ${blueprint.id} : $state produced ${nextStates.size} states: $nextStates")
    return result
}

fun maxGeodes(states: List<MiningState>): MiningState {
    return states.maxByOrNull { (T) -> T.geode }!!
}

data class MiningState(val resources: Resources, val robots: Resources, val timeRemaining: Int)

data class Resources(val ore: Int, val clay: Int, val obsidian: Int, val geode: Int) {
    fun add(other: Resources): Resources {
        return Resources(ore + other.ore, clay + other.clay, obsidian + other.obsidian, geode + other.geode)
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


