import java.awt.Point
import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day24input.txt").readLines()

    val sampleInput = ("sesenwnenenewseeswwswswwnenewsewsw\n" +
            "neeenesenwnwwswnenewnwwsewnenwseswesw\n" +
            "seswneswswsenwwnwse\n" +
            "nwnwneseeswswnenewneswwnewseswneseene\n" +
            "swweswneswnenwsewnwneneseenw\n" +
            "eesenwseswswnenwswnwnwsewwnwsene\n" +
            "sewnenenenesenwsewnenwwwse\n" +
            "wenwwweseeeweswwwnwwe\n" +
            "wsweesenenewnwwnwsenewsenwwsesesenwne\n" +
            "neeswseenwwswnwswswnw\n" +
            "nenwswwsewswnenenewsenwsenwnesesenew\n" +
            "enewnwewneswsewnwswenweswnenwsenwsw\n" +
            "sweneswneswneneenwnewenewwneswswnese\n" +
            "swwesenesewenwneswnwwneseswwne\n" +
            "enesenwswwswneneswsenwnewswseenwsese\n" +
            "wnwnesenesenenwwnenwsewesewsesesew\n" +
            "nenewswnwewswnenesenwnesewesw\n" +
            "eneswnwswnwsenenwnwnwwseeswneewsenese\n" +
            "neswnwewnwnwseenwseesewsenwsweewe\n" +
            "wseweeenwnesenwwwswnew").split("\n")
    val refTileInput = mutableListOf("nwwswee")
    day24Part1(input)
}

enum class TileColor {
    BLACK, WHITE
}
enum class TileDirection {
    e, se, sw, w, nw, ne
}
class FloorTile(private var color: TileColor = TileColor.WHITE ) {
    var flipCount = 0

    fun flip() {
        color = when (color) { TileColor.BLACK -> TileColor.WHITE; TileColor.WHITE -> TileColor.BLACK }
//        println("Flipping tile to $color")
        flipCount++
    }

    fun getColor() : TileColor {
        return color
    }


}

class FloorTileGrid(val referenceTile: FloorTile) {
    // 2D grid, odd rows are shifted right. So 0,1 is the SE neighbor of 0,0
    private var grid = mutableListOf<MutableList<FloorTile>>()
    private var referenceTileCoords = Point(0, 0)

    private var currentTile = referenceTile
    private var currentTileCoords = Point(0, 0)

    fun init(size: Int) {
        for (x in 0 until (size*4)) {
            grid.add(mutableListOf())
            for (y in 0 until (size*4)) {
                grid[x].add(FloorTile())
            }
        }
        grid[size * 2][size * 2] = referenceTile
        referenceTileCoords.x = size * 2
        referenceTileCoords.y = size * 2
    }

    fun moveCurrentTile(direction: TileDirection) {
//        expandGridIfNecessary(direction)
        val oddRow = (currentTileCoords.y % 2) == 1
//        println("moving $direction from $currentTileCoords oddRow: $oddRow")
        var nextX = when (direction) {
            TileDirection.e -> currentTileCoords.x + 1
            TileDirection.se -> if (oddRow) currentTileCoords.x + 1 else currentTileCoords.x
            TileDirection.sw -> if (oddRow) currentTileCoords.x else currentTileCoords.x - 1
            TileDirection.w -> currentTileCoords.x - 1
            TileDirection.nw -> if (oddRow) currentTileCoords.x else currentTileCoords.x - 1
            TileDirection.ne -> if (oddRow) currentTileCoords.x + 1 else currentTileCoords.x
        }
        var nextY = when (direction) {
            TileDirection.e -> currentTileCoords.y
            TileDirection.se -> currentTileCoords.y + 1
            TileDirection.sw -> currentTileCoords.y + 1
            TileDirection.w -> currentTileCoords.y
            TileDirection.nw -> currentTileCoords.y - 1
            TileDirection.ne -> currentTileCoords.y - 1
        }

//        println("moving from $currentTileCoords $direction to $nextX, $nextY ($oddRow)")

        currentTile = grid[nextX][nextY]
        currentTileCoords.x = nextX
        currentTileCoords.y = nextY
    }

    private fun expandGridIfNecessary(direction: TileDirection) {
        // Check ranges and expand the grid if necessary
        // if nextX < 0, insert another column and add 1 to everything
        // if nextX > maxX, add another column
        if (currentTileCoords.x == 0 && (direction == TileDirection.w
                    || direction == TileDirection.nw
                    || direction == TileDirection.sw)) {
            val height = grid[0].size
            grid.add(0, mutableListOf())
            for (i in 0 until height) {
                grid[0].add(FloorTile())
            }
            referenceTileCoords.x += 1
            currentTileCoords.x += 1
        } else if (currentTileCoords.x == (grid.size - 1) && (direction == TileDirection.e
                    || direction == TileDirection.ne
                    || direction == TileDirection.se)) {
            val height = grid[0].size
            grid.add(mutableListOf())
            for (i in 0 until height) {
                grid.last().add(FloorTile())
            }
        }
        if (currentTileCoords.y == 0 && (direction == TileDirection.nw
                    || direction == TileDirection.ne)) {
            // add a row by inserting to the beginning of all columns and
            // add 1 to all y values
            grid.forEach { col ->
                col.add(0, FloorTile())
            }
            referenceTileCoords.y += 1
            currentTileCoords.y += 1
        } else if (currentTileCoords.y == (grid[0].size - 1) && (direction == TileDirection.sw
                    || direction == TileDirection.se)) {
            grid.forEach { col ->
                col.add(FloorTile())
            }
        }
    }

    fun iterate() {
        val copy = mutableListOf<MutableList<FloorTile>>()
        for (x in 0 until grid.size) {
            copy.add(mutableListOf<FloorTile>())
            for (y in 0 until grid[0].size) {
                copy[x].add(FloorTile(grid[x][y].getColor()))
            }
        }

        val height = grid[0].size
        for (x in 0 until grid.size) {
            for (y in 0 until grid[0].size) {
                val oddRow = (y % 2) == 1

                val neighbors = mutableSetOf<FloorTile>()

                for (direction in TileDirection.values()) {
                    var nextX = when (direction) {
                        TileDirection.e -> x + 1
                        TileDirection.se -> if (oddRow) x + 1 else x
                        TileDirection.sw -> if (oddRow) x else x - 1
                        TileDirection.w -> x - 1
                        TileDirection.nw -> if (oddRow) x else x - 1
                        TileDirection.ne -> if (oddRow) x + 1 else x
                    }
                    var nextY = when (direction) {
                        TileDirection.e -> y
                        TileDirection.se -> y + 1
                        TileDirection.sw -> y + 1
                        TileDirection.w -> y
                        TileDirection.nw -> y - 1
                        TileDirection.ne -> y - 1
                    }

                    if (nextX >= 0 && nextX < grid.size
                        && nextY >= 0 && nextY < height) {
                        neighbors.add(grid[nextX][nextY])
                    }
                }
                val blackTiles = neighbors.filter { it.getColor() == TileColor.BLACK }.size
                if (grid[x][y].getColor() == TileColor.BLACK && (blackTiles == 0 || blackTiles > 2)) {
                    copy[x][y].flip()
                } else if (grid[x][y].getColor() == TileColor.WHITE && blackTiles == 2) {
                    copy[x][y].flip()
                }
            }
        }
        grid = copy
    }

    fun resetToReferenceTile() {
        currentTile = referenceTile
        currentTileCoords.x = referenceTileCoords.x
        currentTileCoords.y = referenceTileCoords.y
    }

    fun flipCurrentTile() {
        currentTile.flip()
    }

    fun countBlackTiles() : Int {
        var result = 0
        grid.forEach {col ->
            col.forEach { tile ->
                if (tile.getColor() == TileColor.BLACK) {
                    result++
                }
            }
        }
        return result
    }

    fun size() : Int {
        var result = 0
        grid.forEach {col ->
            col.forEach { tile ->
                result++
            }
        }
        return result
    }

    fun printFlipCounts() {
        val flipCounts = mutableMapOf<Int, Int>()
        grid.forEach {col ->
            col.forEach { tile ->
                if (flipCounts.containsKey(tile.flipCount))
                    flipCounts[tile.flipCount] = flipCounts[tile.flipCount]!! + 1
                else
                    flipCounts[tile.flipCount] = 1
            }
        }
        flipCounts.forEach { (k, v) ->
            println("$v tiles flipped $k times")
        }
    }

    override fun toString(): String {
        val height = grid[0]!!.size!!
        var result = ""
        for (i in 0 until height) {
            if (i != 0 && i % 2 == 1) {
                result += " "
            }
            grid.forEach { col ->
                if (col[i] == referenceTile) {
                    result += "[${if (col[i].getColor() == TileColor.WHITE) "W" else "B"}]"
                } else if (col[i] == currentTile) {
                    result += "(${if (col[i].getColor() == TileColor.WHITE) "W" else "B"})"
                } else {
                    result += " ${if (col[i].getColor() == TileColor.WHITE) "W" else "B"} "
                }
            }
            result += "\n"
        }
        return result
    }
}

fun day24Part1(input: List<String>) {
    var longest = 0
    input.forEach {line ->
        if (line.length > longest) longest = line.length
    }
    val referenceTile = FloorTile()
    val grid = FloorTileGrid(referenceTile)
    grid.init(longest)

    input.forEachIndexed {index, line ->
//        println("line $index")

        var i = 0
        grid.resetToReferenceTile()
//        println(grid)

        while (i < line.length) {
            val direction: TileDirection
            if (line[i] == 's' || line[i] == 'n') {
                direction = TileDirection.valueOf(line.substring(i, i+2))
                i+=2
            } else {
                direction = TileDirection.valueOf(line.substring(i, i+1))
                i+=1
            }
//            println("moving $direction")
            grid.moveCurrentTile(direction)
//            println(grid)
        }

        grid.flipCurrentTile()
    }

    var result = grid.countBlackTiles()

    grid.printFlipCounts()

//    println("grid:\n${grid.toString()}")

    // 262 too low
    // 352 too low
    println("$result black tiles out of ${grid.size()}")

    println("\n\nStarting iterations")
    for (i in 1..100) {
        grid.iterate()
//        if (i >= 30 && i < 35) println(grid)
        println("Day $i: ${grid.countBlackTiles()}")
    }
}
