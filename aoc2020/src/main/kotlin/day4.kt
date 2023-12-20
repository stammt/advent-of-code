import java.io.File

fun main(args: Array<String>) {
    val lines = File("/Users/stammt/dev/aoc/day4input.txt").readLines()

    var passport: String = ""
    var valids = 0
    lines.forEach {
        val line = it.trim()
        if (line.length == 0) {
            val isValid = isValidPassport(passport)
            if (isValid) valids++
            passport = ""
        } else {
            passport += " $line"
        }
    }
    val isValid = isValidPassport(passport)
    if (isValid) valids++

    println("valids: $valids")
}

fun isValidPassport(passport: String) : Boolean {
    val requiredFields = mutableSetOf("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")

//    println("checking $passport")

    val parts = passport.split(" ")
    parts.forEach {

        val subparts = it.split(":")
        if (subparts.size == 2) {
            val key = subparts[0]
            val value = subparts[1]
            val validValue = when (key) {
                "byr" -> validYear(value.toInt(), 1920, 2002)
                "iyr" -> validYear(value.toInt(), 2010, 2020)
                "eyr" -> validYear(value.toInt(), 2020, 2030)
                "hgt" -> validHeight(value)
                "hcl" -> validHairColor(value)
                "ecl" -> validEyeColor(value)
                "pid" -> validPassportId(value)
                else -> false
            }
            print("$it valid is $validValue, ")
            if (validValue) {
                requiredFields.remove(key)
            }
        }
    }
    val isValid = requiredFields.isEmpty()
    println("$isValid :: $passport")
    return requiredFields.isEmpty()
}

fun validYear(year: Int, min: Int, max: Int) : Boolean {
    return year >= min && year <= max
}

fun validHeight(height: String) : Boolean {
    if (height.length < 3) return false;
    val units = height.subSequence(height.length - 2, height.length)
    val value = height.subSequence(0, height.length - 2).toString().toInt()
    return when (units) {
        "cm" -> validYear(value, 150, 193)
        "in" -> validYear(value, 59, 76)
        else -> false
    }
}

fun validHairColor(color: String) : Boolean {
    if (color.length != 7) return false
    if (!color.startsWith("#")) return false
    return color.substring(1, 6).matches(Regex("[0-9a-f]*"))
}

fun validEyeColor(color: String) : Boolean {
    val validColors = setOf("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
    return validColors.contains(color)
}

fun validPassportId(id: String) : Boolean {
    if (id.length != 9) return false;
    return id.matches(Regex("[0-9]*"))
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