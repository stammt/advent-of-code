import java.io.File
import java.lang.IllegalArgumentException
import java.lang.IllegalStateException
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/dev/advent-of-code/aoc2022/input/day22input.txt").readLines()
    day22part2(input)
}

data class Point(val x: Int, val y: Int)
enum class Direction(val point: Point) {
    NORTH(Point(0, -1)),
    SOUTH(Point(0, 1)),
    EAST(Point(1, 0)),
    WEST(Point(-1, 0))
}

fun makeTurn(dir: Point, turn: Char): Point {
    return if (turn == 'L') Point(dir.y, -dir.x) else Point(-dir.y, dir.x)
}

data class EdgeTransition(val face: Int,
                          val pointTransform: (Point) -> Point ,
                          val facing: Direction)
data class Face(
    val position: Point,
    val grid: Map<Point, Char>,
    val northEdge: EdgeTransition,
    val southEdge: EdgeTransition,
    val eastEdge: EdgeTransition,
    val westEdge: EdgeTransition) {

    fun getEdgeTransition(dir: Point): EdgeTransition {
        when (dir) {
            Direction.NORTH.point -> return northEdge
            Direction.SOUTH.point -> return southEdge
            Direction.EAST.point -> return eastEdge
            Direction.WEST.point -> return westEdge
        }
        print("*** unknown direction $dir")
        return northEdge
    }

    fun facePointToMapPoint(p: Point, faceSize: Int): Point {
        return Point(position.x * faceSize + p.x, position.y * faceSize + p.y)
    }
}

fun facingChar(dir: Point): Char {
    return when (dir) {
        Direction.NORTH.point -> '^'
        Direction.SOUTH.point -> 'v'
        Direction.EAST.point -> '>'
        Direction.WEST.point -> '<'
        else -> '.'
    }
}

fun facingScore(dir: Point): Int {
    return when (dir) {
        Direction.NORTH.point -> 3
        Direction.SOUTH.point -> 1
        Direction.EAST.point -> 0
        Direction.WEST.point -> 2
        else -> 0
    }
}

fun day22part2(input: List<String>) {
    val faceSize = 50 // sample=4, input=50
    val faces = readInputFaces(input, faceSize)

    val start = startPoint(input, faceSize, faces)!!
    println("Starting at ${start.second} in face ${start.first.position}")

    val moveLine = input.last { p -> p.trim().isNotEmpty() }
    val moves = mutableListOf<String>()
    var numberAcc = ""
    for (i in moveLine.indices) {
        if (moveLine[i].isDigit()) {
            numberAcc += moveLine[i]
        } else {
            if (numberAcc.isNotEmpty()) {
                moves.add(numberAcc)
                numberAcc = ""
            }
            moves.add(moveLine[i].toString())
        }
    }
    if (numberAcc.isNotEmpty()) {
        moves.add(numberAcc)
    }

    var pos = start
    var facing = Direction.EAST.point
    val overlay = mutableMapOf<Point, Char>()
    for (i in moves.indices) {
        val oldP = pos.second
        val oldMapPoint = pos.first.facePointToMapPoint(oldP, faceSize)
        val oldFacing = facing
        if (moves[i] == "L" || moves[i] == "R") {
            facing = makeTurn(facing, moves[i][0])
            val mapPoint = pos.first.facePointToMapPoint(pos.second, faceSize)
//            println("Move ${moves[i]}: $oldMapPoint ${facingChar(oldFacing)} to $mapPoint facing ${facingChar(facing)}")
            overlay[mapPoint] = facingChar(facing)
        } else {
            val count = moves[i].toInt()
            var p = pos.second
            var face = pos.first
            for (step in 0 until count) {
                var nextPos = Point(p.x + facing.x, p.y + facing.y)
                if (!face.grid.containsKey(nextPos)) {
//                    println("Transition at step $step - $nextPos not in ${face.position}")
                    val edgeTransition = face.getEdgeTransition(facing)
                    nextPos = edgeTransition.pointTransform(p)
                    val nextFacing = edgeTransition.facing.point
                    val nextFace = faces[edgeTransition.face]
//                    println("--- moving to face ${nextFace.position} $nextPos ${facingChar(nextFacing)}")
                    if (nextFace.grid[nextPos] == '.') {
                        p = nextPos
                        facing = nextFacing
                        face = nextFace
                        pos = face to p
                    } else {
//                        println("--- Hit a wall after transition, resetting")
                        break
                    }
                } else if (face.grid[nextPos] == '#') {
//                    println("Hit a wall, stopping at $step")
                    pos = face to p
                    break
                } else {
//                    println("Stepping $step out of $count")
                    p = nextPos
                    pos = face to nextPos
                }
                val mapPoint = pos.first.facePointToMapPoint(pos.second, faceSize)
//                println("Move ${moves[i]}: $oldMapPoint ${facingChar(oldFacing)} to $mapPoint facing ${facingChar(facing)}")
                overlay[mapPoint] = facingChar(facing)
            }
        }
        val mapPoint = pos.first.facePointToMapPoint(pos.second, faceSize)
        println("Move ${moves[i]}: $oldMapPoint ${facingChar(oldFacing)} to $mapPoint facing ${facingChar(facing)}\n")
        overlay[mapPoint] = facingChar(facing)
    }

    printMap(faces, faceSize, overlay)
    val mapPoint = pos.first.facePointToMapPoint(pos.second, faceSize)
    val score = (1000 * (mapPoint.y + 1)) + (4 * (mapPoint.x + 1)) + facingScore(facing)
    println("Ended at $mapPoint with score $score")
    // 148041 too high
    // 15421 too low
    // not 65374
    // not 29515

//    val testOverlay = simpleInputTestCases(faces, faceSize)
//    printMap(faces, faceSize, testOverlay)
}

fun startPoint(input: List<String>, faceSize: Int, faces: List<Face>) : Pair<Face, Point>? {
    for (y in 0 until input.size) {
        for (x in 0 until input[y].length) {
            if (input[y][x] == '.') {
                return mapPointToFacePoint(Point(x, y), faces, faceSize)
            }
        }
    }
    return null
}

fun mapPointToFacePoint(p: Point, faces: List<Face>, faceSize: Int) : Pair<Face, Point> {
    println("$p is in face ${p.x / faceSize}, ${p.y / faceSize}")
    val face = faces.first { f -> f.position == Point(p.x / faceSize, p.y / faceSize) }
    return face to Point(p.x % faceSize, p.y % faceSize)
}

fun printMap(faces: List<Face>, faceSize: Int, overlay: Map<Point, Char>) {
    val projected = mutableMapOf<Point, Char>()
    for (face in faces) {
        for (p in face.grid.keys) {
            projected[face.facePointToMapPoint(p, faceSize)] = face.grid[p]!!
        }
    }
    for (y in 0 until (faceSize * 4)) {
        for (x in 0 until (faceSize * 4)) {
            if (overlay.contains(Point(x, y))) {
                print(overlay[Point(x, y)])
            } else if (projected.containsKey(Point(x, y))) {
                print(projected[(Point(x, y))]);
            } else {
                print(' ')
            }
        }
        println()
    }
    println()
}

fun readInputFaces(input: List<String>, faceSize: Int): List<Face> {
    // There must be a way to figure this out programmatically...
    // - 1 2
    // - 3 -
    // 4 5 -
    // 6 - -
    val face1 = Face(Point(1, 0),
        readGrid(input, (1*faceSize), (2*faceSize), 0, faceSize),
        EdgeTransition(5, { p -> Point(0, p.x) }, Direction.EAST),
        EdgeTransition(2, { p -> Point(p.x, 0)}, Direction.SOUTH),
        EdgeTransition(1, { p -> Point(0, p.y )}, Direction.EAST),
        EdgeTransition(3, { p -> Point(0, faceSize - 1 - p.y)}, Direction.EAST))
    val face2 = Face(Point(2, 0),
        readGrid(input, (faceSize * 2), (faceSize * 3), 0, faceSize),
        EdgeTransition(5, { p -> Point(p.x, faceSize - 1)}, Direction.NORTH),
        EdgeTransition(2, { p -> Point(faceSize - 1, p.x)}, Direction.WEST),
        EdgeTransition(4, { p -> Point(faceSize - 1, faceSize - 1 - p.y)}, Direction.WEST),
        EdgeTransition(0, { p -> Point(faceSize - 1, p.y)}, Direction.WEST))
    val face3 = Face(Point(1, 1),
        readGrid(input, faceSize, faceSize * 2, faceSize, (2*faceSize)),
        EdgeTransition(0, { p -> Point(p.x, faceSize - 1)}, Direction.NORTH),
        EdgeTransition(4, { p -> Point(p.x, 0) }, Direction.SOUTH),
        EdgeTransition(1, { p -> Point(p.y, faceSize - 1) }, Direction.NORTH),
        EdgeTransition(3, { p -> Point(p.y, 0) }, Direction.SOUTH)
    )
    val face4 = Face(Point(0, 2),
        readGrid(input, 0, faceSize, (faceSize * 2), (3*faceSize)),
        EdgeTransition(2, { p -> Point(0, p.x) }, Direction.EAST),
        EdgeTransition(5, { p -> Point(p.x, 0) }, Direction.SOUTH),
        EdgeTransition(4, { p -> Point(0, p.y)}, Direction.EAST),
        EdgeTransition(0, { p -> Point(0, faceSize - 1 - p.y) }, Direction.EAST),
    )
    val face5 = Face(Point(1, 2),
        readGrid(input, faceSize, faceSize * 2, faceSize * 2,faceSize * 3),
        EdgeTransition(2, { p -> Point(p.x, faceSize - 1) }, Direction.NORTH),
        EdgeTransition(5, { p -> Point(faceSize - 1, p.x) }, Direction.WEST),
        EdgeTransition(1, { p -> Point(faceSize - 1, faceSize - 1 - p.y)}, Direction.WEST),
        EdgeTransition(3, { p -> Point(faceSize - 1, p.y) }, Direction.WEST)
    )
    val face6 = Face(Point(0, 3),
        readGrid(input, 0, faceSize, faceSize * 3,faceSize * 4),
        EdgeTransition(3, { p -> Point(p.x, faceSize - 1) }, Direction.NORTH),
        EdgeTransition(1, { p -> Point(p.x, 0) }, Direction.SOUTH),
        EdgeTransition(4, { p -> Point(p.y, faceSize - 1) }, Direction.NORTH),
        EdgeTransition(0, { p -> Point(p.y, 0) }, Direction.SOUTH)
    )

    return listOf(face1, face2, face3, face4, face5, face6)
}


fun readSampleFaces(input: List<String>, faceSize: Int): List<Face> {
    // There must be a way to figure this out programmatically...
    // - - 1 -
    // 2 3 4 -
    // - - 5 6
    val face1 = Face(Point(2, 0),
        readGrid(input, (2*faceSize), (3*faceSize), 0, faceSize),
        EdgeTransition(4, { p -> Point(p.x, faceSize-1) }, Direction.NORTH),
        EdgeTransition(3, { p -> Point(p.x, 0)}, Direction.SOUTH),
        EdgeTransition(5, { p -> Point(faceSize - 1 - p.y, 0)}, Direction.SOUTH),
        EdgeTransition(2, { p -> Point(faceSize - 1, p.y )}, Direction.WEST))
    val face2 = Face(Point(0, 1),
        readGrid(input, 0, faceSize, faceSize, (2*faceSize)),
        EdgeTransition(0, { p -> Point(faceSize - 1 - p.x, 0)}, Direction.SOUTH),
        EdgeTransition(4, { p -> Point(faceSize - 1 - p.x, faceSize - 1)}, Direction.NORTH),
        EdgeTransition(2, { p -> Point(0, p.y)}, Direction.EAST),
        EdgeTransition(5, { p -> Point(faceSize - 1 - p.y, faceSize - 1)}, Direction.NORTH))
    val face3 = Face(Point(1, 1),
        readGrid(input, faceSize, faceSize * 2, faceSize, (2*faceSize)),
        EdgeTransition(0, { p -> Point(0, p.x)}, Direction.EAST),
        EdgeTransition(4, { p -> Point(0, faceSize - 1 - p.x) }, Direction.EAST),
        EdgeTransition(3, { p -> Point(0, p.y) }, Direction.EAST),
        EdgeTransition(1, { p -> Point(faceSize - 1, p.y) }, Direction.WEST)
        )
    val face4 = Face(Point(2, 1),
        readGrid(input, faceSize * 2, faceSize * 3, faceSize, (2*faceSize)),
        EdgeTransition(0, { p -> Point(p.x, faceSize - 1) }, Direction.NORTH),
        EdgeTransition(4, { p -> Point(p.x, 0) }, Direction.SOUTH),
        EdgeTransition(5, { p -> Point(faceSize - 1 - p.y, 0)}, Direction.SOUTH),
        EdgeTransition(2, { p -> Point(faceSize - 1, p.y) }, Direction.WEST),
        )
    val face5 = Face(Point(2, 2),
        readGrid(input, faceSize * 2, faceSize * 3, faceSize * 2,faceSize * 3),
        EdgeTransition(3, { p -> Point(p.x, faceSize - 1) }, Direction.NORTH),
        EdgeTransition(1, { p -> Point(faceSize - 1 - p.x, faceSize - 1) }, Direction.NORTH),
        EdgeTransition(5, { p -> Point(0, p.y)}, Direction.EAST),
        EdgeTransition(2, { p -> Point(faceSize - 1 - p.y, faceSize - 1) }, Direction.NORTH),
    )
    val face6 = Face(Point(3, 2),
        readGrid(input, faceSize * 3, faceSize * 4, faceSize * 2,faceSize * 3),
        EdgeTransition(3, { p -> Point(faceSize - 1, faceSize - 1 - p.x) }, Direction.WEST),
        EdgeTransition(1, { p -> Point(0, faceSize - 1 - p.x) }, Direction.EAST),
        EdgeTransition(0, { p -> Point(faceSize - 1, faceSize - 1 - p.y) }, Direction.WEST),
        EdgeTransition(4, { p -> Point(faceSize - 1, p.y) }, Direction.WEST)
        )

    return listOf(face1, face2, face3, face4, face5, face6)
}

fun readGrid(input: List<String>, startX: Int, stopX: Int, startY: Int, stopY: Int): Map<Point, Char> {
    val grid = mutableMapOf<Point, Char>()
    for (x in startX until stopX)
        for (y in startY until stopY) {
            grid[Point(x-startX,y-startY)] = input[y][x]
        }

    return grid
}

fun sampleTestCases(faces: List<Face>, faceSize: Int) {
    val a = Point(11, 5)
    val aFacePoint = mapPointToFacePoint(a, faces, faceSize)
    println("$a mapped to $aFacePoint")
    val bFacePoint = aFacePoint.first.eastEdge.pointTransform(aFacePoint.second)
    val bFace = faces [aFacePoint.first.eastEdge.face]
    val b = bFace.facePointToMapPoint(bFacePoint, faceSize)

    val c = Point(10, 11)
    val cFacePoint = mapPointToFacePoint(c, faces, faceSize)
    val dFacePoint = cFacePoint.first.southEdge.pointTransform(cFacePoint.second)
    val dFace = faces[cFacePoint.first.southEdge.face]
    val d = dFace.facePointToMapPoint(dFacePoint, faceSize)
}

fun simpleInputTestCases(faces: List<Face>, faceSize: Int): Map<Point, Char> {
    // north/south 1, 2, 3, 4, 5, 6
    val a = Point(1, 12)
    val aFacePoint = mapPointToFacePoint(a, faces, faceSize)
    println("$a mapped to $aFacePoint")
    val bFacePoint = aFacePoint.first.northEdge.pointTransform(aFacePoint.second)
    val bFace = faces [aFacePoint.first.northEdge.face]
    val b = bFace.facePointToMapPoint(bFacePoint, faceSize)
    println("Going north from $a went to $bFacePoint facing ${facingChar(aFacePoint.first.northEdge.facing.point)} in $bFace")

    val c = Point(2, 15)
    val cFacePoint = mapPointToFacePoint(c, faces, faceSize)
    println("$c mapped to $cFacePoint")
    val dFacePoint = cFacePoint.first.southEdge.pointTransform(cFacePoint.second)
    val dFace = faces[cFacePoint.first.southEdge.face]
    val d = dFace.facePointToMapPoint(dFacePoint, faceSize)
    println("Going south from $c went to $dFacePoint facing ${facingChar(cFacePoint.first.southEdge.facing.point)} in $dFace")

//    // east/west 1, 2, 3, 4, 5, 6
//    val a = Point(7, 9)
//    val aFacePoint = mapPointToFacePoint(a, faces, faceSize)
//    println("$a mapped to $aFacePoint")
//    val bFacePoint = aFacePoint.first.eastEdge.pointTransform(aFacePoint.second)
//    val bFace = faces [aFacePoint.first.eastEdge.face]
//    val b = bFace.facePointToMapPoint(bFacePoint, faceSize)
//    println("Going east from $a went to $bFacePoint facing ${facingChar(aFacePoint.first.eastEdge.facing.point)} in $bFace")
//
//    val c = Point(4, 10)
//    val cFacePoint = mapPointToFacePoint(c, faces, faceSize)
//    println("$c mapped to $cFacePoint")
//    val dFacePoint = cFacePoint.first.westEdge.pointTransform(cFacePoint.second)
//    val dFace = faces[cFacePoint.first.westEdge.face]
//    val d = dFace.facePointToMapPoint(dFacePoint, faceSize)
//    println("Going west from $c went to $dFacePoint facing ${facingChar(cFacePoint.first.westEdge.facing.point)} in $dFace")

    return mapOf(a to 'A', b to 'B', c to 'C', d to 'D')
}

fun day22part1(input: List<String>) {
    val board = mutableMapOf<Pair<Int, Int>, Char>()
    val turns = mutableListOf<String>()
    var i = 0
    while (input[i].isNotBlank()) {
        for (x in input[i].indices) {
            if (input[i][x] == '.' || input[i][x] == '#') {
                board[x to i] = input[i][x]
            }
        }
        i++
    }
    i++
    var x = 0
    var turn = ""
    while (x < input[i].length) {
        if (input[i][x].isDigit()) {
            turn += input[i][x]
        } else {
            turns.add(turn)
            turn = ""
            turns.add("" + input[i][x])
        }
        x++
    }
    turns.add(turn)

    println("Board: $board")
    println("Turns: $turns")

    val minX = board.filter{ it.key.second == 0 && board[it.key] == '.'  }.map { it.key.first }.min()

    var facing = 0
    var pos = minX to 0
    println("Starting at $pos")
    for (turn in turns) {
        if (turn[0].isDigit()) {
            pos = move(turn.toInt(), pos, facing, board)
        } else {
            facing = turn(turn, facing)
        }
    }

    var result = (1000 * (pos.second + 1)) + (4 * (pos.first + 1)) + facing
    println("Result $result ($pos facing $facing)")
}

fun turn(dir: String, facing: Int) : Int {
    val next = if (dir == "R") facing + 1 else facing - 1
    return if (next > 3) 0 else if (next < 0) 3 else next
}

fun move(count: Int, pos: Pair<Int, Int>, facing: Int, board: Map<Pair<Int, Int>, Char>) : Pair<Int, Int> {
    var nextPos = pos
    for (i in 0 until count) {
        val maxX = board.filter{it.key.second == nextPos.second  }.map { it.key.first }.max()
        val minX = board.filter{it.key.second == nextPos.second }.map { it.key.first }.min()
        val maxY = board.filter{it.key.first == nextPos.first }.map { it.key.second }.max()
        val minY = board.filter{it.key.first == nextPos.first }.map { it.key.second }.min()
        println("For $nextPos $minX $minY and $maxX $maxY")
        var nextX = nextPos.first
        var nextY = nextPos.second
        if (facing == 0) {
            nextX++
            if (nextX > maxX) {
                nextX = minX
            }
        } else if (facing == 2) {
            nextX--
            if (nextX < minX) {
                nextX = maxX
            }
        } else if (facing == 1) {
            nextY++
            if (nextY > maxY) {
                nextY = minY
            }
        } else if (facing == 3) {
            nextY--
            if (nextY < minY) {
                nextY = maxY
            }
        } else {
            throw IllegalArgumentException("Unknown facing $facing")
        }

        if (board[nextX to nextY] == '#') {
            println("Would hit a wall")
            break
        } else {
            println("Stepping to $nextX,$nextY")
            nextPos = nextX to nextY
        }
    }
    println("Moved from $pos to $nextPos facing $facing")
    return nextPos
}


