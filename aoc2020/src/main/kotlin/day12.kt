import java.io.File
import java.time.Duration
import java.time.Instant
import kotlin.math.abs

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day12input.txt").readLines()

    day12Part2(input)  // 58637
}

fun day12Part2(input : List<String>) {
    var shipX = 0
    var shipY = 0
    var waypointX = 10
    var waypointY = 1

    input.forEach{
        var action = it[0]
        val distance = it.substring(1).toInt()

        when (action) {
            'R', 'L' -> {
                val turns = (distance % 360) / 90
                for (i in 0 until turns) {
                    val oldX = waypointX
                    val oldY = waypointY
                    if (action == 'R') {
                        waypointX = oldY
                        waypointY = oldX * -1
                    } else {
                        waypointX = oldY * -1
                        waypointY = oldX
                    }
                }
            }
            'N' -> waypointY += distance
            'S' -> waypointY -= distance
            'E' -> waypointX += distance
            'W' -> waypointX -= distance
            'F' -> {
                shipX += (waypointX * distance)
                shipY += (waypointY * distance)
            }
            else -> println("don't know how to handle $it $action")
        }
    }

    val distance = abs(shipX) + abs(shipY)
    println("ended at $shipX , $shipY distance $distance")
}


fun day12Part1(input : List<String>) {
    var x = 0
    var y = 0
    var heading = 0

    input.forEach{
        var action = it[0]
        val distance = it.substring(1).toInt()

        if (action == 'F') {
            action = when(heading) {
                0 -> 'E'
                90, -270 -> 'S'
                180, -180 -> 'W'
                270, -90 -> 'N'
                else -> 'X'
            }
            println("heading is $heading forward is $action")
        }
        when (action) {
            'L' -> heading = (heading - distance) % 360
            'R' -> heading = (heading + distance) % 360
            'N' -> y += distance
            'S' -> y -= distance
            'E' -> x += distance
            'W' -> x -= distance
            else -> println("don't know how to handle $it $action")
        }
    }

    val distance = abs(x) + abs(y)
    println("ended at $x , $y distance $distance")
}

