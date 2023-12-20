import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/Documents/2022aoc/day07input.txt").readLines()
//    val input = File("/Users/stammt/Documents/2022aoc/day07sample.txt").readLines()
//    val input = listOf(
//    )

//    parseCrates(input)
    day07part1(input)
}

fun day07part1(input: List<String>) {
    var root = DirEntry("/", null)
    var currentDir: DirEntry = root

    var i = 0
    while (i < input.size) {
        val line = input[i++]
        val tokens = line.split(" ")
        if (tokens[0] == "$") {
            if (tokens[1] == "cd") {
                if (tokens[2] == "/") {
                    currentDir = root
                } else if (tokens[2] == "..") {
                    currentDir = currentDir.parent!!
                } else if (currentDir.dirs.containsKey(tokens[2])) {
                    currentDir = currentDir.dirs[tokens[2]]!!
                } else {
                    println("adding dir ${tokens[2]} by cd")
                    val dir = DirEntry(tokens[2], currentDir)
                    currentDir.dirs[tokens[2]] = dir
                    currentDir = dir
                }
            } else if (tokens[1] == "ls") {
                // consume until the next command, or we run out of lines
                while (i < input.size && !input[i].startsWith("$")) {
                    val ls = input[i++].split(" ")
                    if (ls[0] == "dir") {
                        val name = ls[1]
                        if (!currentDir.dirs.containsKey(name)) {
                            val dir = DirEntry(name, currentDir)
                            currentDir.dirs[name] = dir
                        }
                    } else {
                        val size = ls[0].toInt()
                        val name = ls[1]
                        currentDir.files[name] = size
                    }
                }
            } else {
                println("unknown command ${tokens[1]}")
            }
        }
    }

//    println("structure: \n $root")
//    println("root totalSize ${root.totalSize()}")

//    val smallDirs = root.getSmallDirs()
//    val result = smallDirs.map { it.totalSize() }.sum()
//    println("result: $result out of ${smallDirs.size} small dirs")
    val totalSize = 70000000
    val requiredSize = 30000000
    val usedSize = root.totalSize()
    val freeSpace = totalSize - usedSize
    val needToFree = requiredSize - freeSpace
    println("Need to free $needToFree")

    val allDirSizes = root.getAllDirSizes()
    val sortedDirSizes = allDirSizes.sorted()
    val size = sortedDirSizes.first { it >= needToFree }
    println("would free $size")
}

data class DirEntry(val name: String, val parent: DirEntry?) {
    val dirs = mutableMapOf<String, DirEntry>()
    val files = mutableMapOf<String, Int>()

    fun getSmallDirs() : List<DirEntry> {
        val list = mutableListOf<DirEntry>()
        list.addAll(dirs.values.filter { it.totalSize() <= 100000 })
        for (d in dirs) {
            list.addAll(d.value.getSmallDirs())
        }
        return list
    }

    fun totalSize() : Int {
        var size = 0
        for (d in dirs) {
            size += d.value.totalSize()
        }
        for (f in files) {
            size += f.value
        }
        return size
    }

    fun getAllDirSizes() : List<Int> {
        val list = mutableListOf(totalSize())
        for (d in dirs) {
            list.addAll(d.value.getAllDirSizes())
        }
        return list
    }


    override fun toString() : String {
        return toString(0)
    }

    private fun toString(depth: Int) : String {
        var result = ""
        for (i in 0 .. depth) {
            result += (" ")
        }
        result += ("- $name (dir)")
        result += (" totalSize=${totalSize()}\n")
        for (d in dirs) {
            result += d.value.toString(depth + 1)
        }
        for (f in files) {
            for (i in 0 .. depth+1) {
                result += (" ")
            }
            result += ("- ${f.key} (file, size=${f.value})\n")
        }
        result += "\n"
        return result
    }


}