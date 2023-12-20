import java.io.File
import java.lang.IllegalArgumentException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
//    val input = File("/Users/stammt/Documents/2022aoc/day19input.txt").readLines()
    val input = File("/Users/stammt/Documents/2022aoc/day19sample.txt").readLines()
    day19part1(input)
}

fun day19part1(input: List<String>) {
    val blueprints = parseBlueprints(input)

    var qualityTotal = 0
    for (i in blueprints.indices) {
        val geodes = maxGeodes(blueprints[i])
        val quality = (i+1) * geodes
        qualityTotal += quality
        println("blueprint $i has $geodes (quality $quality)")
    }

    // 977 too low
    println("quality total $qualityTotal")
}

fun maxGeodes(blueprint: Blueprint) : Int {
    val time = 0
    val workingRobots = mutableMapOf("ore" to 1)
    val resources = mutableMapOf<String, Int>()

    for (time in 1..24) {
        println("== Minute $time ==")

        val build = shouldBuild(blueprint, workingRobots, resources)

        if (build != null) {
            // Spend resources building a robot
            val robot = blueprint.robots[build]!!
            println("Spend ${robot.costs} to build $build")
            for (cost in robot.costs) {
                resources[cost.key] = resources[cost.key]!! - cost.value
            }
        }

        // Add resources that were mined this round
        for (m in workingRobots) {
            resources[m.key] = resources[m.key]?.plus(m.value) ?: m.value
            println("Collect ${m.value} ${m.key}; now have ${resources[m.key]}")
        }

        // Add the new bot
        if (build != null) {
            workingRobots[build] = workingRobots[build]?.plus(1) ?: 1
            println("Added new $build bot, now have ${workingRobots[build]}")
        }
        println()
    }
    return resources["geode"] ?: 0
}

fun maxGeodesForOption(blueprint: Blueprint, resources: Map<String, Int>, workingRobots: Map<String, Int>, time: Int) : Int {
    if (time == 2) {
        val geodes = resources["geode"] ?: 0
//        println("Returning $geodes at $time (with $resources and bots $workingRobots)")
        return geodes
    }

    // See what robots we can build in this minute. Branch for doing nothing, or building any possible robots.
    // This is in a loop in case we can build multiple of the same kind of robot.
    val geodeCounts = mutableListOf<Int>()
    val noBuildingOption = maxGeodesForOption(blueprint, addResources(resources, workingRobots), workingRobots, time+1)
    geodeCounts.add(noBuildingOption)



    val potentialBots = canBuildRobots(resources, blueprint)
    if (potentialBots.isEmpty()) {
        return maxGeodesForOption(blueprint, addResources(resources, workingRobots), workingRobots, time+1)
    } else {
        //    println("Time $time: $blueprint can build $potentialBots with $resources")
        for (bot in potentialBots) {
            val resourcesAfterBuilding = buildRobot(resources, bot)
            val resourcesAfterBuildingAndMining = addResources(resourcesAfterBuilding, workingRobots)

            val workingRobotsAfterBuilding = workingRobots.toMutableMap()
            workingRobotsAfterBuilding[bot.resource] = workingRobots[bot.resource]?.plus(1) ?: 1
            //        println("Time $time: built a ${bot.resource} bot, had $resources not have $resourcesAfterBuilding")
            //        println(">> working bots $workingRobots now have $resourcesAfterBuildingAndMining")
            if (bot.resource == "obsidian" || bot.resource == "geode") {
                println(">>> time $time: building ${bot.resource} now have $workingRobotsAfterBuilding")
            }
            val option =
                maxGeodesForOption(blueprint, resourcesAfterBuildingAndMining, workingRobotsAfterBuilding, time + 1)
            geodeCounts.add(option)
        }

        return geodeCounts.max()
    }
}

fun canBuildRobots(resources: Map<String, Int>, blueprint: Blueprint) : List<Robot> {
    // see what robots we can build with the available resources
    val robots = mutableListOf<Robot>()
    for (r in blueprint.robots) {
        if (canAffordRobot(resources, r.value)) {
            robots.add(r.value)
        }
    }
    return robots
}

fun canAffordRobot(resources: Map<String, Int>, robot: Robot) : Boolean {
    for (cost in robot.costs) {
        val amt = resources[cost.key]
        if (amt == null || amt < cost.value) {
            return false
        }
    }
    return true
}

// Return the resources left over after building this robot
fun buildRobot(resources: Map<String, Int>, robot: Robot) : Map<String, Int> {
    val updatedResources = resources.toMutableMap()
    for (cost in robot.costs) {
        updatedResources[cost.key] = resources[cost.key]!! - cost.value
    }
    return updatedResources
}

fun addResources(resources: Map<String, Int>, mined: Map<String, Int>) : Map<String, Int> {
    val totals = resources.toMutableMap()
    for (m in mined) {
        totals[m.key] = totals[m.key]?.plus(m.value) ?: m.value
    }
    return totals
}

fun shouldBuild(blueprint: Blueprint, workingRobots: Map<String, Int>, resources: Map<String, Int>) : String? {
    // See what the next needed bot is at this point.
    val nextNeededBot = "geode"

//        if (!workingRobots.containsKey("clay")) "clay"
//        else if (!workingRobots.containsKey("obsidian")) "obsidian"
//        else "geode" // always need more geode bots!

    println("Next needed bot: $nextNeededBot")

    // Then see if it would be faster if we had another lower bot, or if we
    // should just continue mining. This might recurse, e.g. if an obsidian
    // bot is needed, it might be fastest to make another "ore" bot.
    var build = getBotToBuildNow(nextNeededBot, blueprint, workingRobots, resources)
    if (build == null) {
        println("Best to wait and mine")
        return null
    } else if (canAffordRobot(resources, blueprint.robots[build]!!)) {
        return build
    } else {
        println("Need a $build but can't afford yet")
        return null
    }
}

fun getBotToBuildNow(neededBot: String, blueprint: Blueprint, workingRobots: Map<String, Int>, resources: Map<String, Int>) : String? {
    if (neededBot == "clay") {
        return nextBotToGetClayBot(blueprint, workingRobots, resources)
    } else if (neededBot == "obsidian") {
        return nextBotToGetObsidianBot(blueprint, workingRobots, resources)
    } else {
        return nextBotToGetGeodeBot(blueprint, workingRobots, resources)
    }
}

fun nextBotToGetClayBot(blueprint: Blueprint, workingRobots: Map<String, Int>, resources: Map<String, Int>) : String? {
    // If we can build it now, do it
    if (canAffordRobot(resources, blueprint.robots["clay"]!!)) return "clay"

    // Otherwise see if we should build an ore bot
    if (!canAffordRobot(resources, blueprint.robots["ore"]!!)) return null

    val oreCost = blueprint.robots["clay"]!!.costs["ore"]!!
    val neededOre = max(0, oreCost - (resources["ore"] ?: 0))

    val orePerMinute = (workingRobots["ore"] ?: 0)
    val minutesNeededNoBot = neededOre / orePerMinute

    val oreBotCost = blueprint.robots["ore"]!!.costs["ore"]!!
    val minutesNeededWithBot = ((neededOre + oreBotCost - orePerMinute) / (orePerMinute + 1)) + 1
    println("Would need $minutesNeededNoBot to build a clay bot, or $minutesNeededWithBot to build another ore bot first")
    return if (minutesNeededNoBot < minutesNeededWithBot) null else "ore"
}

fun nextBotToGetObsidianBot(blueprint: Blueprint, workingRobots: Map<String, Int>, resources: Map<String, Int>) : String? {
    // If we can build it now, do it
    if (canAffordRobot(resources, blueprint.robots["obsidian"]!!)) return "obsidian"

    // need to see if it's faster to wait, build an ore bot, or build a clay bot
    val oreCost = blueprint.robots["obsidian"]!!.costs["ore"]!!
    val neededOre = max(0, oreCost - (resources["ore"] ?: 0))
    val clayCost = blueprint.robots["obsidian"]!!.costs["clay"]!!
    val neededClay = max(0, clayCost - (resources["clay"] ?: 0))

    val orePerMinute = (workingRobots["ore"] ?: 0)
    val clayPerMinute = (workingRobots["clay"] ?: 0)
    val minutesNeededNoBot = if (clayPerMinute == 0) Int.MAX_VALUE else  max(neededOre / orePerMinute, neededClay / clayPerMinute)

    var minutesNeededWithOreBot = Int.MAX_VALUE
//    if (canAffordRobot(resources, blueprint.robots["ore"]!!)) {
    val oreBotCost = blueprint.robots["ore"]!!.costs["ore"]!!
    val oreBotClayTime = if (clayPerMinute == 0) Int.MAX_VALUE else neededClay / clayPerMinute
    minutesNeededWithOreBot = max(
        ((neededOre + oreBotCost - orePerMinute) / (orePerMinute + 1)) + 1,
        oreBotClayTime
    )
//    }

    var minutesNeededWithClayBot = Int.MAX_VALUE
//    if (canAffordRobot(resources, blueprint.robots["clay"]!!)) {
    // Clay bots cost ore but produce clay
    val clayBotCost = blueprint.robots["clay"]!!.costs["ore"]!!
    minutesNeededWithClayBot = max(
        (neededOre + clayBotCost) / orePerMinute,
        ((neededClay - clayPerMinute) / (clayPerMinute + 1)) + 1
    )
//    }

    println("Need an obsidian bot: would take $minutesNeededNoBot, with ore bot $minutesNeededWithOreBot, with clay bot $minutesNeededWithClayBot")
    return if (minutesNeededWithClayBot <= minutesNeededWithOreBot &&
        minutesNeededWithClayBot <= minutesNeededNoBot) {
        // We need a clay bot, check the fastest way to get one of those
        nextBotToGetClayBot(blueprint, workingRobots, resources)
    } else if (minutesNeededWithOreBot <= minutesNeededWithClayBot &&
            minutesNeededWithOreBot <= minutesNeededNoBot) {
            "ore"
    } else {
        null
    }

//    return if (minutesNeededWithOreBot < minutesNeededWithClayBot &&
//        minutesNeededWithOreBot < minutesNeededNoBot) {
//        "ore"
//    } else if (minutesNeededWithClayBot < minutesNeededWithOreBot &&
//            minutesNeededWithClayBot < minutesNeededNoBot) {
//        // We need a clay bot, check the fastest way to get one of those
//        nextBotToGetClayBot(blueprint, workingRobots, resources)
//    } else {
//        null
//    }
}

fun nextBotToGetGeodeBot(blueprint: Blueprint, workingRobots: Map<String, Int>, resources: Map<String, Int>) : String? {
    // If we can build it now, do it
    if (canAffordRobot(resources, blueprint.robots["geode"]!!)) return "geode"

    // need to see if it's faster to wait or build another bot
    val oreCost = blueprint.robots["geode"]!!.costs["ore"]!!
    val neededOre = max(0,  oreCost - (resources["ore"] ?: 0))
//    val clayCost = 0// blueprint.robots["geode"]!!.costs["clay"]!!
//    val neededClay = 0 //clayCost - (resources["clay"] ?: 0)
    val obsidianCost = blueprint.robots["geode"]!!.costs["obsidian"]!!
    val neededObsidian = max(0, obsidianCost - (resources["obsidian"] ?: 0))

    val orePerMinute = (workingRobots["ore"] ?: 0)
//    val clayPerMinute = (workingRobots["clay"] ?: 0)
    val obsidianPerMinute = (workingRobots["obsidian"] ?: 0)
    val minutesNeededNoBot = if (orePerMinute == 0 || obsidianPerMinute == 0)
        Int.MAX_VALUE else max(neededOre / orePerMinute,
        neededObsidian / obsidianPerMinute)

    var minutesNeededWithOreBot = Int.MAX_VALUE
//    if (canAffordRobot(resources, blueprint.robots["ore"]!!)) {
        val oreBotCost = blueprint.robots["ore"]!!.costs["ore"]!!
        val oreBotOreTime = ((neededOre + oreBotCost - orePerMinute) / (orePerMinute + 1)) + 1
        val oreBotObsidianTime = if (obsidianPerMinute == 0) Int.MAX_VALUE else neededObsidian / obsidianPerMinute
        minutesNeededWithOreBot = max(oreBotOreTime, oreBotObsidianTime)

//    }


    var minutesNeededWithObsidianBot = Int.MAX_VALUE
//    if (canAffordRobot(resources, blueprint.robots["obsidian"]!!)) {
        // Geode bots cost ore and clay but produce obsidian
        val obsidianBotCostOre = blueprint.robots["obsidian"]!!.costs["ore"]!!
        val obsidianBotCostClay = blueprint.robots["obsidian"]!!.costs["clay"]!!
        minutesNeededWithObsidianBot = max((neededOre + obsidianBotCostOre) / orePerMinute,
            ((neededObsidian - obsidianPerMinute) / (obsidianPerMinute + 1)) + 1)
//    }

    println("Need a geode bot: would take $minutesNeededNoBot, with ore bot $minutesNeededWithOreBot, with obsidian bot $minutesNeededWithObsidianBot")
    return if (minutesNeededWithObsidianBot <= minutesNeededNoBot &&
            minutesNeededWithObsidianBot <= minutesNeededWithOreBot) {
        nextBotToGetObsidianBot(blueprint, workingRobots, resources)
    } else if (minutesNeededWithOreBot <= minutesNeededWithObsidianBot &&
        minutesNeededWithOreBot <= minutesNeededNoBot) {
        "ore"
    } else {
        null
    }
}

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
        blueprints.add(Blueprint(id+1, robots))
    }

    return blueprints
}


data class Blueprint(val id: Int, val robots: Map<String, Robot>) {
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
