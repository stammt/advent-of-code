import java.io.File

fun main(args: Array<String>) {
    val a = countTrees(1, 1);
    val b = countTrees(3, 1)
    val c = countTrees(5, 1)
    val d = countTrees(7, 1)
    val e = countTrees(1, 2)

    val answer = a*b*c*d*e
    println("$a $b $c $d $e :: $answer")
}

fun countTrees(x: Int, y:Int) : Int {
    val lines = File("/Users/stammt/dev/aoc/day3input.txt").readLines()
    val rows = lines.size
    val cols = lines[0].length
    println("$rows x $cols")

    var trees: Int = 0
    var row: Int = 0
    var col: Int = 0

    row += y;
    while (row < rows) {
        col = (col + x) % cols
        if (lines[row][col].equals('#')) trees++
        row += y;
    }

    println("trees: $trees")
    return trees
}



//File("/Users/stammt/dev/day2input.txt").forEachLine { println(it) }

//val lines = File("/Users/stammt/dev/day2input.txt").readLines()
//var valids = 0;
//lines.forEach({
//    val parts = it.split(":", " ", "-")
//    val min = parts[0].toInt() - 1
//    val max = parts[1].toInt() - 1
//    val letter = parts[2][0]
//    val password = parts[4].trim();
//
//    var count = 0;
//    if (password.length > min && password[min].equals(letter)) count++;
//    if (password.length > max && password[max].equals(letter)) count++;
//    if (count == 1) valids++;
////    val count = password.count({it.equals(letter)});
////    val result = count >= min && count <= max;
////    if (result ) valids++;
//    //println(it + " >> " + result + " pwd " + max + " count was " + count)
//})
//
//println("valids " + valids + " out of " + lines.size)