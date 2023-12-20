import java.awt.Point
import java.io.File
import java.lang.Math.floor
import java.time.Duration
import java.time.Instant
import kotlin.math.abs
import kotlin.math.sqrt

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day20input.txt").readLines()
//    val input = File("/Users/stammt/dev/aoc/day20sample.txt").readLines()

    day20Part2(input)
}

class Tile(val id: Int, val lines: List<String>) {
    val topEdgeHashCode = topEdge().hashCode()
    val topEdgeReversedHashCode = topEdge().reversed().hashCode()
    val bottomEdgeHashCode = bottomEdge().hashCode()
    val bottomEdgeReversedHashCode = bottomEdge().reversed().hashCode()
    val rightEdgeHashCode = rightEdge().hashCode()
    val rightEdgeReversedHashCode = rightEdge().reversed().hashCode()
    val leftEdgeHashCode = leftEdge().hashCode()
    val leftEdgeReversedHashCode = leftEdge().reversed().hashCode()
    private val allEdgeVariations = setOf(topEdgeHashCode, topEdgeReversedHashCode,
        bottomEdgeHashCode, bottomEdgeReversedHashCode,
        leftEdgeHashCode, leftEdgeReversedHashCode,
        rightEdgeHashCode, rightEdgeReversedHashCode)

    fun stripBorders() : List<String> {
        return lines.subList(1, lines.size - 1).map { it.substring(1, it.length - 1)}
    }

    fun canMatchAnyEdge(other: Tile) : Boolean {
        return allEdgeVariations.contains(other.topEdgeHashCode)
                || allEdgeVariations.contains(other.bottomEdgeHashCode)
                || allEdgeVariations.contains(other.leftEdgeHashCode)
                || allEdgeVariations.contains(other.rightEdgeHashCode)
    }

    fun topEdge() : String {
        return lines[0]
    }

    fun bottomEdge() : String {
        return lines.last()
    }

    fun leftEdge() : String {
        return lines.map { it[0] }.joinToString("")
    }

    fun rightEdge() : String {
        return lines.map { it.last() }.joinToString("")
    }

    fun flipOnVerticalAxis() : Tile {
        val flippedLines = lines.map { it.reversed() }
        return Tile(id, flippedLines)
    }

    fun flipOnHorizontalAxis() : Tile {
        val flippedLines = lines.reversed()
        return Tile(id, flippedLines)
    }

    fun rotate(turns: Int) : Tile {
        /*
        1 2 3
        4 5 6
        7 8 9

        7 4 1
        8 5 2
        9 6 3

        9 8 7
        6 5 4
        3 2 1
         */

        var flippedLines: List<String> = lines
        for (t in 0 until turns) {
            var resultLines = MutableList<String>(lines.size) { "" }
            for (x in 0 until lines.size) {
                for (y in (lines.size - 1) downTo 0) {
                    resultLines[x] = resultLines[x] + flippedLines[y][x]
                }
            }
            flippedLines = resultLines
        }
        return Tile(id, flippedLines)
    }

    override fun toString(): String {
        return when (id) {
            0 -> "0000"
            else -> id.toString()
        }
    }
}

class TileGrid(val tileCount: Int) {
    private val nullTile = Tile(0, List(10) { List(10) { "." }.joinToString { " " }})
    private val arrangedSize = sqrt(tileCount.toDouble()).toInt()
    private val arranged = Array(arrangedSize) { Array(arrangedSize) { nullTile} }

    fun build(inputTiles: List<Tile>) : Boolean {
        val tiles = inputTiles.toMutableList()
        val corners = findCorners(tiles).toMutableList()

        println("found ${corners.size} corners (${corners.map { it.id }}")
        println("arrangedSize = $arrangedSize")
        tiles.removeAll(corners)

        // find a corner with a match for its right edge, start that at 0,0
        var firstCorner: Tile? = null
        for (corner in corners) {
            val match1 = findRightEdgeMatch(corner, tiles)
            val match2 = findBottomEdgeMatch(corner, tiles)
            if (match1 != null && match2 != null) {
                firstCorner = corner
                break
            }
        }
        if (firstCorner == null) {
            println("didn't find a first corner!")
            return false
        }
        corners.remove(firstCorner)

        // arbitrarily start from the first tile, then build left-to-right from
        // there, then repeat for each row. At the end of the first row will be
        // another corner.
        arranged[0][0] = firstCorner
        for (i in 1 until (arrangedSize - 1)) {
            // find a tile with an edge that matches the last tile's right edge
            val tile = arranged[i - 1][0]
            println("*** $i matching right edge of tile ${tile.id} (${tile.rightEdge()}}")

            val match = findRightEdgeMatch(tile, tiles)
            if (match != null) {
                println("found match with ${match.id}")
                arranged[i][0] = match
                tiles.removeIf { it.id == match.id }
            }
        }
        // end of the row, find the next corner
        val cornerMatch = findRightEdgeMatch(arranged[arrangedSize - 2][0], corners)
        if (cornerMatch == null) {
            println("couldn't find top last corner!")
            return false
        }
        arranged[arrangedSize - 1][0] = cornerMatch
        corners.removeIf { it.id == cornerMatch.id }

        // for the next rows, start with a bottom match and move on to the right
        // no corners
        for (y in 1 until (arrangedSize - 1)) {
            for (x in 0 until arrangedSize) {
                val tile = arranged[x][y-1]
                println("looking for bottom match for ${tile.id}")
                val match = findBottomEdgeMatch(tile, tiles)
                if (match != null) {
                    println("found bottom match of ${match.id} matches ${tile.id}")
                    arranged[x][y] = match
                    tiles.removeIf{ it.id == match.id}
                }
            }
        }

        // last row, find corner matches and then fill in
        val bottomFirstCornerMatch = findBottomEdgeMatch(arranged[0][arrangedSize-2], corners)
        if (bottomFirstCornerMatch == null) {
            println("couldn't find bottom first corner!")
            return false
        }
        arranged[0][arrangedSize-1] = bottomFirstCornerMatch
        corners.removeIf { bottomFirstCornerMatch.id == it.id }

        for (i in 1 until (arrangedSize - 1)) {
            val tile = arranged[i - 1][arrangedSize - 1]
            println("*** $i matching right edge of tile ${tile.id} (${tile.rightEdge()}}")

            val match = findRightEdgeMatch(tile, tiles)
            if (match != null) {
                println("found match with ${match.id}")
                arranged[i][arrangedSize-1] = match
                tiles.removeIf { it.id == match.id }
            }
        }
        // then should be the final corner, double check
        if (corners.size != 1) {
            println("too many corners?")
            return false
        }

        val lastMatch = findRightEdgeMatch(arranged[arrangedSize-2][arrangedSize-1], corners)
        if (lastMatch == null) {
            println("couldn't fit the last corner")
            return false
        }
        if (lastMatch.id != corners[0].id) {
            println("wrong corner?")
            return false
        }
        arranged[arrangedSize-1][arrangedSize-1] = lastMatch

        return true
    }

    fun stripBordersAndMerge() : List<String> {
        val lines = mutableListOf<String>()
        val tileLineCount = arranged[0][0].lines.size - 2 // strip first and last
        for (y in 0 until arrangedSize) {
            for (i in 0 until (tileLineCount)) {
                lines.add("")
                for (x in 0 until arrangedSize) {
                    val lineIndex = (y*tileLineCount) + (i )
                    val line = arranged[x][y].lines[i+1]
                    lines[lineIndex] = lines[lineIndex] + line.substring(1, line.length - 1)
                }
            }
        }
        return lines
    }

    fun findRightEdgeMatch(tile: Tile, tiles: List<Tile>) : Tile? {
        for (candidate in tiles) {
            println("checking tile ${candidate.id}")
            val match: Tile? = when (tile.rightEdgeHashCode) {
                candidate.leftEdgeHashCode -> candidate
                candidate.leftEdgeReversedHashCode -> candidate.flipOnHorizontalAxis()
                candidate.rightEdgeHashCode -> candidate.flipOnVerticalAxis()
                candidate.rightEdgeReversedHashCode -> candidate.flipOnVerticalAxis().flipOnHorizontalAxis()
                candidate.topEdgeHashCode -> candidate.rotate(1).flipOnVerticalAxis()
                candidate.topEdgeReversedHashCode -> candidate.rotate(3)
                candidate.bottomEdgeHashCode -> candidate.rotate(1)
                candidate.bottomEdgeReversedHashCode -> candidate.rotate(1).flipOnHorizontalAxis()
                else -> null
            }
            if (match != null) {
                return match
            }
        }
        return null
    }

    fun findBottomEdgeMatch(tile: Tile, tiles: List<Tile>) : Tile? {
        println("find match for bottom edge ${tile.bottomEdge()}")
        for (candidate in tiles) {
            println("checking tile ${candidate.id}")
            val match: Tile? = when (tile.bottomEdgeHashCode) {
                candidate.leftEdgeHashCode -> candidate.rotate(1).flipOnVerticalAxis()
                candidate.leftEdgeReversedHashCode -> candidate.rotate(1)
                candidate.rightEdgeHashCode -> candidate.rotate(3)
                candidate.rightEdgeReversedHashCode -> candidate.rotate(3).flipOnVerticalAxis()
                candidate.topEdgeHashCode -> candidate
                candidate.topEdgeReversedHashCode -> candidate.flipOnVerticalAxis()
                candidate.bottomEdgeHashCode -> candidate.flipOnHorizontalAxis()
                candidate.bottomEdgeReversedHashCode -> candidate.flipOnHorizontalAxis().flipOnVerticalAxis()
                else -> null
            }
            if (match != null) {
                return match
            }
        }
        return null
    }

    override fun toString(): String {
        var line = ""
        for (y in 0 until arrangedSize) {
            for (x in 0 until arrangedSize) {
                line += (" ${arranged[x][y]} ")
            }
            line += "\n"
        }
        return line
    }
}

fun findCorners(tiles: List<Tile>) : List<Tile> {
    val corners = mutableListOf<Tile>()

    for (tile in tiles) {
        var matches = 0;

        for (candidate in tiles) {
            if (candidate == tile) continue

            if (tile.canMatchAnyEdge(candidate)) matches++

        }
        if (matches == 2) {
            corners.add(tile)
        }
    }
    return corners
}

fun day20Part2(input: List<String>) {
    var startTime = System.currentTimeMillis()

    val tiles = mutableListOf<Tile>()
    var currentTile = mutableListOf<String>()
    var currentTileId = 0
    input.forEach {
        val line = it.trim()
        if (line.startsWith("Tile ")) {
            if (currentTileId != 0) {
                tiles.add(Tile(currentTileId, currentTile))
            }
            currentTileId = line.substring(5, line.length - 1).toInt()
            currentTile = mutableListOf()
        } else if (!line.isEmpty()) {
            currentTile.add(line)
        }
    }
    tiles.add(Tile(currentTileId, currentTile))

    val grid = TileGrid(tiles.size)
    grid.build(tiles)

    println("grid so far: \n $grid")

    val mergedLines = grid.stripBordersAndMerge()
    println("merged:")
    for (mergedLine in mergedLines) {
        println(mergedLine)
    }

    // make a tile from this so we can transform it easily
    val mergedTile = Tile(0, mergedLines)

    val seaMonsterPattern = listOf(
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    )
    val seaMonsterPoints = seaMonsterCoordinates(seaMonsterPattern)
    val seaMonsterWidth = seaMonsterPattern[0].length
    val seaMonsterHeight = seaMonsterPattern.size

    val count = doItAll(mergedTile, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    if (count != 0) {
        println("found $count monsters!")
        // 15 '#' in each monster

        var totalHashes = 0
        for (line in mergedTile.lines) {
            for (c in line) {
                if (c == '#') totalHashes++
            }
        }

        val hashCount = totalHashes - (count * 15)
        println("hashCount $hashCount") //1665
    }

    var endTime = System.currentTimeMillis()
    println("runtime ${endTime - startTime}ms")
}

fun doItAll(mergedTile: Tile, seaMonsterPoints: List<Point>, seaMonsterWidth: Int, seaMonsterHeight: Int) : Int {
    // try a bunch of transformations...
    var count = 0
    val flippedOnHoriz = mergedTile.flipOnHorizontalAxis()
    count = findSeaMonsters(flippedOnHoriz.lines, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    println("$count in flippedOnHoriz")
    if (count != 0) return count;
    count = findSeaMonstersRotated(flippedOnHoriz, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    if (count != 0) return count;

    val flippedOnVert = mergedTile.flipOnVerticalAxis()
    count = findSeaMonsters(flippedOnVert.lines, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    println("$count in flippedOnVert")
    if (count != 0) return count;
    count = findSeaMonstersRotated(flippedOnVert, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    if (count != 0) return count;

    val flippedHV = mergedTile.flipOnHorizontalAxis().flipOnVerticalAxis()
    count = findSeaMonsters(flippedHV.lines, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    println("$count in flippedHV")
    if (count != 0) return count;
    count = findSeaMonstersRotated(flippedHV, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    if (count != 0) return count;

    val flippedVH = mergedTile.flipOnVerticalAxis().flipOnHorizontalAxis()
    count = findSeaMonsters(flippedVH.lines, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    println("$count in flippedVH")
    if (count != 0) return count;
    count = findSeaMonstersRotated(flippedVH, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    if (count != 0) return count;

    count = findSeaMonstersRotated(mergedTile, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
    return count
}

fun findSeaMonstersRotated(tile: Tile, seaMonsterPoints: List<Point>, seaMonsterWidth: Int, seaMonsterHeight: Int) : Int {
    var count = 0
    for (r in 0..3) {
        val rotated = tile.rotate(r)
        val rcount = findSeaMonsters(rotated.lines, seaMonsterPoints, seaMonsterWidth, seaMonsterHeight)
        println("$rcount in rotate $r")
        count = maxOf(count, rcount)
    }
    return count
}

fun findSeaMonsters(lines: List<String>, seaMonsterPattern: List<Point>, seaMonsterWidth: Int, seaMonsterHeight: Int) : Int {
    val windowSlopHoriz = lines[0].length - seaMonsterWidth
    val windowSlopVert = lines.size - seaMonsterHeight

    // slide around a window the size of a sea monster, look for a match
    var count = 0
    for (x in 0..windowSlopHoriz) {
        for (y in 0..windowSlopVert) {
            var matchedPoints = 0
            for (p in seaMonsterPattern) {
                if (lines[y + p.y][x + p.x] == '#') matchedPoints++
            }
            if (matchedPoints == seaMonsterPattern.size) {
                println("found monster at $x, $y")
                count++
            }
        }
    }
    return count
}

fun seaMonsterCoordinates(seaMonsterPattern: List<String>) : List<Point> {
    val points = mutableListOf<Point>()
    for (i in 0 until seaMonsterPattern.size) {
        val line = seaMonsterPattern[i]
        for (j in 0 until line.length) {
            if (line[j] == '#') {
                points.add(Point(j, i))
            }
        }
    }
    return points
}


fun day20Part1(input: List<String>) {
    var startTime = System.currentTimeMillis()

    val tiles = mutableListOf<Tile>()
    var currentTile = mutableListOf<String>()
    var currentTileId = 0
    input.forEach {
        val line = it.trim()
        if (line.startsWith("Tile ")) {
            if (currentTileId != 0) {
                tiles.add(Tile(currentTileId, currentTile))
            }
            currentTileId = line.substring(5, line.length - 1).toInt()
            currentTile = mutableListOf()
        } else if (!line.isEmpty()) {
            currentTile.add(line)
        }
    }
    tiles.add(Tile(currentTileId, currentTile))

    val x = tiles.last()
    println("tile ${x.id}")
    println("topEdge: ${x.topEdge()}")
    println("bottomEdge: ${x.bottomEdge()}")
    println("rightEdge: ${x.rightEdge()}")
    println("leftEdge: ${x.leftEdge()}")
    println("---")

    // there should be 4 tiles that have a top/bottom and right/left edge that does
    // not match any other tile
    val corners = findCorners(tiles)

    var endTime = System.currentTimeMillis()
    println(corners.map { it.id })
    println("found ${corners.size} corners in ${endTime - startTime}ms")

    if (corners.size == 4) {
        var result = corners[0].id.toLong() * corners[1].id.toLong() * corners[2].id.toLong() * corners[3].id.toLong()
        println("result = $result")
    }

}
