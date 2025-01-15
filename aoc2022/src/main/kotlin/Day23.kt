import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day23input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day23sample.txt").readLines()
    day23part2(input)
}

fun day23part2(input: List<String>) {
    val map = mutableMapOf<Pair<Int, Int>, Elf>()
    for (y in input.indices) {
        for (x in input[y].indices) {
            if (input[y][x] == '#') {
                map[x to y] = Elf(x to y)
            }
        }
    }

    // for each move track the list of elfs that propose to move to each
    // location, then for any proposals with only one elf, update the
    // main map
    val proposals = mutableMapOf<Pair<Int, Int>, MutableSet<Elf>>()
    val directions = mutableListOf(NORTH, SOUTH, WEST, EAST)

    var result = -1
    for (turn in 1..10000) {
        var moved = false
        for (elf in map) {
            val move = elf.value.proposeMove(elf.key, directions, map)
            if (move != null) {
                val others = proposals[move]
                if (others == null) {
                    proposals[move] = mutableSetOf(elf.value)
                } else {
                    others.add(elf.value)
                }
            }
        }

        for (elf in proposals) {
            if (elf.value.size == 1) {
                var elfToMove = elf.value.asIterable().first()
                map.remove(elfToMove.pos)
                elfToMove.pos = elf.key
                map[elf.key] = elfToMove
                moved = true
            }
        }
        if (!moved) {
            result = turn
            break
        }

//        println("=== Round $turn checking $directions")
//        println("=== End of round $turn ===")
//        printMap(map)
//        println()

        proposals.clear()

        // move the first direction check to the end of the list
        var check = directions.removeAt(0)
        directions += check
    }
    println("First round with no moves: $result")
}


fun day23part1(input: List<String>) {
    val map = mutableMapOf<Pair<Int, Int>, Elf>()
    for (y in input.indices) {
        for (x in input[y].indices) {
            if (input[y][x] == '#') {
                map[x to y] = Elf(x to y)
            }
        }
    }

    // for each move track the list of elfs that propose to move to each
    // location, then for any proposals with only one elf, update the
    // main map
    val proposals = mutableMapOf<Pair<Int, Int>, MutableSet<Elf>>()
    val directions = mutableListOf(NORTH, SOUTH, WEST, EAST)

    for (turn in 1..10) {
        for (elf in map) {
            val move = elf.value.proposeMove(elf.key, directions, map)
            if (move != null) {
                val others = proposals[move]
                if (others == null) {
                    proposals[move] = mutableSetOf(elf.value)
                } else {
                    others.add(elf.value)
                }
            }
        }

        for (elf in proposals) {
            if (elf.value.size == 1) {
                var elfToMove = elf.value.asIterable().first()
                map.remove(elfToMove.pos)
                elfToMove.pos = elf.key
                map[elf.key] = elfToMove
            }
        }

//        println("=== Round $turn checking $directions")
//        println("=== End of round $turn ===")
//        printMap(map)
//        println()

        proposals.clear()

        // move the first direction check to the end of the list
        var check = directions.removeAt(0)
        directions += check
    }

    val minX = map.map { it.key.first }.min()
    val maxX = map.map { it.key.first }.max()
    val minY = map.map { it.key.second }.min()
    val maxY = map.map { it.key.second }.max()

    val totalMapSize = (minX..maxX).count() * (minY..maxY).count()
    val emptySquares = totalMapSize - map.size

    printMap(map)

    println("Empty squares: $emptySquares out of $totalMapSize ($minX to $maxX by $minY to $maxY)")
}

fun printMap(map: Map<Pair<Int, Int>, Elf>) {
    val minX = map.map { it.key.first }.min()
    val maxX = map.map { it.key.first }.max()
    val minY = map.map { it.key.second }.min()
    val maxY = map.map { it.key.second }.max()

    for (y in minY..maxY) {
        for (x in minX..maxX) {
            val c = if (map.containsKey(x to y)) '#' else '.'
            print(c)
        }
        println()
    }
}

interface Direction23 {
    fun getFrom(pos: Pair<Int, Int>) : Pair<Int, Int>
}

enum class CardinalDirection : Direction23 {
    N {
        override fun getFrom(pos: Pair<Int, Int>): Pair<Int, Int> {
                return pos.first to pos.second - 1
        }
    },
    NE {
        override fun getFrom(pos: Pair<Int, Int>): Pair<Int, Int> {
            return pos.first + 1 to pos.second - 1
        }
    },
    NW {
        override fun getFrom(pos: Pair<Int, Int>): Pair<Int, Int> {
            return pos.first - 1 to pos.second - 1
        }
    },
    S {
        override fun getFrom(pos: Pair<Int, Int>): Pair<Int, Int> {
            return pos.first to pos.second + 1
        }
    },
    SE {
        override fun getFrom(pos: Pair<Int, Int>): Pair<Int, Int> {
            return pos.first + 1 to pos.second + 1
        }
    },
    SW {
        override fun getFrom(pos: Pair<Int, Int>): Pair<Int, Int> {
            return pos.first - 1 to pos.second + 1
        }
    },
    E {
        override fun getFrom(pos: Pair<Int, Int>): Pair<Int, Int> {
            return pos.first + 1 to pos.second
        }
    },
    W {
        override fun getFrom(pos: Pair<Int, Int>): Pair<Int, Int> {
            return pos.first - 1 to pos.second
        }
    },
}

data class DirectionCheck(val move: Direction23, val checks: List<Direction23>) {
}

val NORTH = DirectionCheck(CardinalDirection.N, listOf(CardinalDirection.N, CardinalDirection.NE, CardinalDirection.NW))
val SOUTH = DirectionCheck(CardinalDirection.S, listOf(CardinalDirection.S, CardinalDirection.SE, CardinalDirection.SW))
val EAST = DirectionCheck(CardinalDirection.E, listOf(CardinalDirection.E, CardinalDirection.NE, CardinalDirection.SE))
val WEST = DirectionCheck(CardinalDirection.W, listOf(CardinalDirection.W, CardinalDirection.NW, CardinalDirection.SW))

class Elf(var pos: Pair<Int, Int>) {
    fun proposeMove(pos: Pair<Int, Int>, directions: List<DirectionCheck>, map: Map<Pair<Int, Int>, Elf>) : Pair<Int, Int>? {
        // If no elves are adjacent, don't do anything
        var found = false
        for (d in CardinalDirection.values()) {
            val otherPos = d.getFrom(pos)
            if (map.containsKey(otherPos)) {
                found = true
                break
            }
        }
        if (!found) {
            return null
        }

        // check each direction in order, and move to the first one
        // that did not find another elf.
        var proposal: Pair<Int, Int>? = null
        for (d in directions) {
            var found = false
            for (check in d.checks) {
                val otherPos = check.getFrom(pos)
                if (map.containsKey(otherPos)) {
                    found = true
                    break
                }
            }
            if (!found) {
                proposal = d.move.getFrom(pos)
                break
            }
        }

        return proposal
    }
}
