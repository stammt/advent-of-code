import java.io.File
import java.time.Duration
import java.time.Instant

fun main(args: Array<String>) {
    val text = File("/Users/stammt/dev/aoc/day11input.txt").readLines()
//    val text = listOf(
//    "L.LL.LL.LL",
//    "LLLLLLL.LL",
//    "L.L.L..L..",
//    "LLLL.LL.LL",
//    "L.LL.LL.LL",
//    "L.LLLLL.LL",
//    "..L.L.....",
//    "LLLLLLLLLL",
//    "L.LLLLLL.L",
//    "L.LLLLL.LL",
//    );
    val rows = text.map { it.toCharArray().toTypedArray() }.toTypedArray()
    day11Part2(rows) // 2064
}

fun day11Part2(rows: Array<Array<Char>>) {
    // deep copy
    var originalRows = rows.map { it.copyOf() }.toTypedArray()
    var updatedRows = rows.map { it.copyOf() }.toTypedArray()

    var iterations = 0
    var changed = false
    do {
        changed = false
        originalRows.forEachIndexed { row, cols ->
            cols.forEachIndexed { col, c ->
//                println("checking $row, $col : ${occupiedVisibleSeats(originalRows, row, col)}")
                when (c) {
                    'L' -> {
                        if (occupiedVisibleSeats(originalRows, row, col) == 0) {
                            changed = true
                            updatedRows[row][col] = '#'
                        }
                    }
                    '#' -> {
                        if (occupiedVisibleSeats(originalRows, row, col) >= 5) {
                            changed = true
                            updatedRows[row][col] = 'L'
                        }
                    }
                }
            }
        }
        // deep copy back into the original
        originalRows = updatedRows.map { it.copyOf() }.toTypedArray()
        iterations++
        println("iterations $iterations")
//        originalRows.forEach { println(it.joinToString()) }
    } while (changed)

    var occupied = 0
    originalRows.forEach{ occupied += it.filter { it == '#' }.size}

    println("$occupied occupied seats after $iterations iterations")
}

fun occupied(rows: Array<Array<Char>>, row: Int, col: Int) : Int {
    return when(rows[row][col]) {
        '#' -> 1
        'L' -> 0
        else -> -1
    }
}

fun firstVisible(rows: Array<Array<Char>>, row: Int, col: Int, dx: Int, dy: Int) : Int {
    var r = row
    var c = col

    r += dy
    c += dx
    while (r >= 0 && r < rows.size && c >= 0 && c < rows[r].size) {
        val occupied = occupied(rows, r, c)
        if (occupied != -1) {
            return occupied
        }
        r += dy
        c += dx
    }
    return 0
}

fun occupiedVisibleSeats(rows: Array<Array<Char>>, row: Int, col: Int) : Int {
    var count = 0;

    count += firstVisible(rows, row, col, 0, -1)
    count += firstVisible(rows, row, col, 1, -1)
    count += firstVisible(rows, row, col, 1, 0)
    count += firstVisible(rows, row, col, 1, 1)
    count += firstVisible(rows, row, col, 0, 1)
    count += firstVisible(rows, row, col, -1, 1)
    count += firstVisible(rows, row, col, -1, 0)
    count += firstVisible(rows, row, col, -1, -1)

    return count
}


fun day11Part1(rows: Array<Array<Char>>) {
    // deep copy
    var originalRows = rows.map { it.copyOf() }.toTypedArray()
    var updatedRows = rows.map { it.copyOf() }.toTypedArray()

    var iterations = 0
    var changed = false
    do {
        changed = false
        originalRows.forEachIndexed { row, cols ->
            cols.forEachIndexed { col, c ->
//                println("checking $row, $col : ${occupiedAdjacentSeats(originalRows, row, col)}")
                when (c) {
                    'L' -> {
                        if (occupiedAdjacentSeats(originalRows, row, col) == 0) {
                            changed = true
                            updatedRows[row][col] = '#'
                        }
                    }
                    '#' -> {
                        if (occupiedAdjacentSeats(originalRows, row, col) >= 4) {
                            changed = true
                            updatedRows[row][col] = 'L'
                        }
                    }
                }
            }
        }
        // deep copy back into the original
        originalRows = updatedRows.map { it.copyOf() }.toTypedArray()
        iterations++
        println("iterations $iterations")
//        originalRows.forEach { println(it.joinToString()) }
    } while (changed)

    var occupied = 0
    originalRows.forEach{ occupied += it.filter { it == '#' }.size}

    println("$occupied occupied seats after $iterations iterations")
}

fun occupiedAdjacentSeats(rows: Array<Array<Char>>, row: Int, col: Int) : Int {
    var count = 0;
    if (row > 0) {
        val r = row - 1;
        if (col > 0) {
            if (rows[r][col - 1] == '#') count++;
        }
        if (rows[r][col] == '#') count++;
        if (col < rows[r].size - 1) {
            if (rows[r][col+1] == '#') count++;
        }
    }

    if (col > 0) {
        if (rows[row][col-1] == '#') count++
    }
    if (col < rows[row].size - 1) {
        if (rows[row][col+1] == '#') count++
    }

    if (row < rows.size - 1) {
        val r = row + 1;
        if (col > 0) {
            if (rows[r][col - 1] == '#') count++;
        }
        if (rows[r][col] == '#') count++;
        if (col < rows[r].size - 1) {
            if (rows[r][col+1] == '#') count++;
        }
    }

    return count
}


