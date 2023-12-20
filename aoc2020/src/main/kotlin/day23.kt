import java.io.File

fun main(args: Array<String>) {
//    val input = File("/Users/stammt/dev/aoc/day23input.txt").readLines()

//    val input = ("Player 1:\n" +
//            "9\n" +
//            "2\n" +
//            "6\n" +
//            "3\n" +
//            "1\n" +
//            "\n" +
//            "Player 2:\n" +
//            "5\n" +
//            "8\n" +
//            "4\n" +
//            "7\n" +
//            "10").split("\n")

//    val input = "389125467".toCharArray()

    val input = "598162734".toCharArray()
    day23Part1Again(input.map { ("" + it).toLong() }.toMutableList())
}

class LinkedListNode(val value: Long) {
    var next: LinkedListNode? = null
    var prev: LinkedListNode? = null

}

class CircularLinkedList(var center: LinkedListNode) {
    fun find(value: Long) : LinkedListNode? {
        var n = center
        do {
            if (n.value == value) return n
            n = n.next!!
        } while (n != center)
        return null
    }

    override fun toString(): String {
        var n:LinkedListNode = center
        var s = ""
        do {
            s += " ${n.value}"
            n = n.next!!
        } while (n != center)
        return s
    }
}

fun day23Part1Again(input: List<Long>) {
    val nodeMap = mutableMapOf<Long, LinkedListNode>()
    var maxValue = input[0]
    var center = LinkedListNode(input[0].toLong())
    nodeMap[input[0]] = center

    var prev = center
    for (i in 1 until input.size) {
        val node = LinkedListNode(input[i].toLong())
        prev.next = node
        node.prev = prev
        prev = node
        if (input[i] > maxValue) {
            maxValue = input[i]
        }
        nodeMap[input[i]] = node
    }
    val x = 1000000
    for (i in (input.size+1) .. x) {
        var node = LinkedListNode(i.toLong())
        prev.next = node
        node.prev = prev
        prev = node
        if (i > maxValue) {
            maxValue = i.toLong()
        }
        nodeMap[i.toLong()] = node
    }
    center.prev = prev
    prev.next = center

    println("total count ${nodeMap.size}")

    val list = CircularLinkedList(center)
//    println("list: $list ")

    val startTime = System.currentTimeMillis()
    for (move in 1..(x*10)) {

        // remove the next three after the center, by relinking their neighbors
        val one = list.center.next!!
        val two = one.next!!
        val three = two.next!!
        list.center.next = three.next!!
        three.next!!.prev = list.center

        // find the destination node
        var destinationValue = list.center.value - 1
        if (destinationValue == 0L) destinationValue = maxValue
        while (destinationValue == one.value ||
                destinationValue == two.value ||
                destinationValue == three.value) {
            destinationValue -= 1
            if (destinationValue == 0L) destinationValue = maxValue
        }
        var destinationNode = nodeMap[destinationValue]

        // insert the other values by relinking the destination node's neighbors
        destinationNode!!.next!!.prev = three
        three.next = destinationNode.next
        destinationNode.next = one
        one.prev = destinationNode

        // move the center to the next node
        list.center = list.center.next!!
    }

//    println("final list: $list")

    // part 1:
//    val oneNode = list.find(1)
//    var result = ""
//    var n = oneNode!!.next
//    while (n != oneNode) {
//        result += n!!.value
//        n = n.next
//    }
//    println("result: $result")

//    // part 2:
    val endTime = System.currentTimeMillis()

    val oneNode = list.find(1)
    val a = oneNode!!.next!!.value
    val b = oneNode!!.next!!.next!!.value
    val result = oneNode!!.next!!.value.toLong() * oneNode.next!!.next!!.value.toLong()
    println("result: $a x $b =  $result in ${endTime - startTime}ms")
}




fun day23Part2x(input: List<Int>) {
    val x = 1000000
    val cups = arrayOfNulls<Int>(x)
    for (i in 0 until input.size) {
        cups[i] = input[i]
    }
    for (i in input.size until x) {
        cups[i] = i
    }

    val highestValue = x
    println("size ${cups.size}")

    val tempCups = arrayOfNulls<Int>(cups.size - 3)
    val buf = arrayOfNulls<Int>(cups.size)


    var i = 0
    for (turn in 0 until (x * 10)) {
        if (turn % 1000 == 0) {
            println("-- move $turn --")
//            printCups(cups, i)
        }
        val currentValue = cups[i]!!

        var removeOneIndex = (i+1) % cups.size
        var removeTwoIndex = (i+2) % cups.size
        var removeThreeIndex = (i+3) % cups.size

        val removeOneValue = cups[removeOneIndex]
        val removeTwoValue = cups[removeTwoIndex]
        val removeThreeValue = cups[removeThreeIndex]

//        println("removing $removeOneIndex ($removeOneValue), $removeTwoIndex ($removeTwoValue), $removeThreeIndex ($removeThreeValue)")

        if (removeOneIndex < removeThreeIndex) {
            // copy before and after removed cups into the temp array
            var tempIndex = 0
            if (removeOneIndex > 0) {
                System.arraycopy(cups, 0, tempCups, 0, removeOneIndex)
                tempIndex = removeOneIndex
            }
            System.arraycopy(cups, removeThreeIndex+1, tempCups, tempIndex, cups.size - removeThreeIndex - 1)
        } else {
            // copy between removed index 3 and removed index 1 into the temp array
            System.arraycopy(cups, removeThreeIndex+1, tempCups, 0, cups.size - 3)
        }

//        println("temp cups: ${tempCups.toList()} ")



        // find the value of the destination
        var destinationValue = currentValue - 1
        if (destinationValue == 0) destinationValue = highestValue
        while (destinationValue == removeOneValue ||
            destinationValue == removeTwoValue ||
            destinationValue == removeThreeValue) {
            destinationValue -= 1
            if (destinationValue == 0) destinationValue = highestValue
        }

        // find the index of the destination
        val destinationIndex = tempCups.indexOf(destinationValue)
//        println("destination index $destinationIndex ($destinationValue)")

        // TODO - copy back so that the "center" cup is still at index i in the cups array
        val tempCenter = tempCups.indexOf(currentValue)
        var dstIndex = i
        var srcIndex = tempCenter

        // copy into the buffer
        // start at tempCenter, go until the end of the temp cups array or
        // the destination, whichever comes first
        var bufIndex = 0
        if (destinationIndex > srcIndex) {
            val firstCopyLen = (destinationIndex - srcIndex + 1)
            System.arraycopy(tempCups, srcIndex, buf, 0, firstCopyLen)
            srcIndex = (srcIndex + firstCopyLen) % tempCups.size
            bufIndex += firstCopyLen

            // add in the removed values
            buf[bufIndex++] = removeOneValue
            buf[bufIndex++] = removeTwoValue
            buf[bufIndex++] = removeThreeValue

            // add the rest of the temp cups array
            val secondCopyLen = (tempCups.size - destinationIndex - 1)
            System.arraycopy(tempCups, srcIndex, buf, bufIndex, secondCopyLen)

            // then copy in the part before the "center" cup
            if (tempCenter != 0) {
                bufIndex += secondCopyLen
                System.arraycopy(tempCups, 0, buf, bufIndex, tempCenter)
            }
//            println("buf (case 1) ${buf.toList()}")
        } else {
            // copy from the "center" to the end of the temp array
            val firstCopyLen = (tempCups.size - srcIndex)
            System.arraycopy(tempCups, srcIndex, buf, 0, firstCopyLen)
            bufIndex += firstCopyLen

            // copy from the beginning of the temp array to the destination index
            val midCopyLen = destinationIndex + 1
            System.arraycopy(tempCups, 0, buf, bufIndex, midCopyLen)
            bufIndex += midCopyLen

            // add in the removed values
            buf[bufIndex++] = removeOneValue
            buf[bufIndex++] = removeTwoValue
            buf[bufIndex++] = removeThreeValue

            // then copy in the part from the destination to the "center" cup
            System.arraycopy(tempCups, destinationIndex+1, buf, bufIndex, tempCenter-destinationIndex-1)
//            println("buf (case 2) ${buf.toList()}")

        }

        // now it's all in the buffer, starting at the "center"
        // copy back into cups, and wrap
        val len = cups.size - i
        System.arraycopy(buf, 0, cups, i, len)
        if (i > 0) {
            System.arraycopy(buf, len, cups, 0, cups.size - len)
        }

        i = (i+1) % cups.size
//        println("---")

    }

    println("cups ${cups.toList()}")

    val one = cups.indexOf(1)
//    val two = cups[(one + 1) % cups.size]!!
//    val three = cups[(one + 2) % cups.size]!!
//    val result = two * three
//    println("result: $result")

    var j = one
    println("one $one")
    var result = ""
    while (result.length < cups.size - 1) {
        j++
        var j = j % cups.size
        result += cups[j]
    }
    println("result: $result")
}


fun day23Part1(input: List<Int>) {
//    val original = input.toList()

    val x = 1000000
    val cups = arrayOfNulls<Int>(input.size)
    for (i in 0 until input.size) {
        cups[i] = input[i]
    }
//    for (i in input.size until x) {
//        cups[i] = i
//    }

    val highestValue = 9 //cups.toList().
    println("size ${cups.size}")

    val tempCups = arrayOfNulls<Int>(cups.size - 3)
    val buf = arrayOfNulls<Int>(cups.size)

    var i = 0
    for (turn in 0 until 100) {
        println("-- move $turn --")
        printCups(cups, i)
        val currentValue = cups[i]!!

        var removeOneIndex = (i+1) % cups.size
        var removeTwoIndex = (i+2) % cups.size
        var removeThreeIndex = (i+3) % cups.size

        val removeOneValue = cups[removeOneIndex]
        val removeTwoValue = cups[removeTwoIndex]
        val removeThreeValue = cups[removeThreeIndex]

        println("removing $removeOneIndex ($removeOneValue), $removeTwoIndex ($removeTwoValue), $removeThreeIndex ($removeThreeValue)")

        if (removeOneIndex < removeThreeIndex) {
            // copy before and after removed cups into the temp array
            var tempIndex = 0
            if (removeOneIndex > 0) {
                System.arraycopy(cups, 0, tempCups, 0, removeOneIndex)
                tempIndex = removeOneIndex
            }
            System.arraycopy(cups, removeThreeIndex+1, tempCups, tempIndex, cups.size - removeThreeIndex - 1)
        } else {
            // copy between removed index 3 and removed index 1 into the temp array
            System.arraycopy(cups, removeThreeIndex+1, tempCups, 0, cups.size - 3)
        }

//        println("temp cups: ${tempCups.toList()} ")



        // find the value of the destination
        var destinationValue = currentValue - 1
        if (destinationValue == 0) destinationValue = highestValue
        while (destinationValue == removeOneValue ||
                destinationValue == removeTwoValue ||
                destinationValue == removeThreeValue) {
            destinationValue -= 1
            if (destinationValue == 0) destinationValue = highestValue
        }

        // find the index of the destination
        val destinationIndex = tempCups.indexOf(destinationValue)
        println("destination index $destinationIndex ($destinationValue)")

        // TODO - copy back so that the "center" cup is still at index i in the cups array
        val tempCenter = tempCups.indexOf(currentValue)
        var dstIndex = i
        var srcIndex = tempCenter

        // copy into the buffer
        // start at tempCenter, go until the end of the temp cups array or
        // the destination, whichever comes first
        var bufIndex = 0
        if (destinationIndex > srcIndex) {
            val firstCopyLen = (destinationIndex - srcIndex + 1)
            System.arraycopy(tempCups, srcIndex, buf, 0, firstCopyLen)
            srcIndex = (srcIndex + firstCopyLen) % tempCups.size
            bufIndex += firstCopyLen

            // add in the removed values
            buf[bufIndex++] = removeOneValue
            buf[bufIndex++] = removeTwoValue
            buf[bufIndex++] = removeThreeValue

            // add the rest of the temp cups array
            val secondCopyLen = (tempCups.size - destinationIndex - 1)
            System.arraycopy(tempCups, srcIndex, buf, bufIndex, secondCopyLen)

            // then copy in the part before the "center" cup
            if (tempCenter != 0) {
                bufIndex += secondCopyLen
                System.arraycopy(tempCups, 0, buf, bufIndex, tempCenter)
            }
            println("buf (case 1) ${buf.toList()}")
        } else {
            // copy from the "center" to the end of the temp array
            val firstCopyLen = (tempCups.size - srcIndex)
            System.arraycopy(tempCups, srcIndex, buf, 0, firstCopyLen)
            bufIndex += firstCopyLen

            // copy from the beginning of the temp array to the destination index
            val midCopyLen = destinationIndex + 1
            System.arraycopy(tempCups, 0, buf, bufIndex, midCopyLen)
            bufIndex += midCopyLen

            // add in the removed values
            buf[bufIndex++] = removeOneValue
            buf[bufIndex++] = removeTwoValue
            buf[bufIndex++] = removeThreeValue

            // then copy in the part from the destination to the "center" cup
            System.arraycopy(tempCups, destinationIndex+1, buf, bufIndex, tempCenter-destinationIndex-1)
            println("buf (case 2) ${buf.toList()}")

        }

        // now it's all in the buffer, starting at the "center"
        // copy back into cups, and wrap
        val len = cups.size - i
        System.arraycopy(buf, 0, cups, i, len)
        if (i > 0) {
            System.arraycopy(buf, len, cups, 0, cups.size - len)
        }

        i = (i+1) % cups.size
    }

    println("cups ${cups.toList()}")

    val one = cups.indexOf(1)
//    val two = cups[(one + 1) % cups.size]!!
//    val three = cups[(one + 2) % cups.size]!!
//    val result = two * three
//    println("result: $result")

    var j = one
    println("one $one")
    var result = ""
    while (result.length < cups.size - 1) {
        j++
        var j = j % cups.size
        result += cups[j]
    }
    println("result: $result")
}

fun day23Part1x(input: MutableList<Int>) {
    val original = input.toList()

    //fill in the input to 1 million
//    val x = 10000 // 8154068
    val x = 10000
    for (x in 10..x) {
        input.add(x)
    }

    println("size ${input.size}")

    var i = 0
    for (turn in 0 until (x*10)) {
//        println("turn $turn")
//        printCups(input, i)


        if (turn > 0 && input.subList(0, original.size) == original) {
            println("repeats at turn $turn")
            break
        } else if (turn % 1000 == 0) {
            val one = input.indexOf(1)
            val two = input[(one + 1) % input.size]
            val three = input[(one + 2) % input.size]
            val result = two * three
            println("turn $turn ($one)  $two x $three == $result")

            // with 100000 elements:
            // turns 1000-43000 3x4=12, 1 was at the end of the list
            // from 44000 3x6=18, 1 started moving down the list by 2250 every 1000 rounds
            // then back around to 99994 with 3x6=18
            // then at 88000 9x14 = 126, 1 moves down the list by 1125 every 1000 rounds
        }

        val currentValue = input[i]
        val removed = mutableListOf<Int>()
        var removeIndex = i
//        print("$turn:  ")
        while (removed.size < 3) {
            removeIndex++
            if (removeIndex >= input.size) removeIndex %= input.size
//            print(" removing $removeIndex (${input[removeIndex]})")
            removed.add(input[removeIndex])
        }
        input.removeAll(removed)
//        println("removed: $removed")

        var destinationValue = currentValue
        var destinationIndex = -1
        do {
            destinationValue -= 1
            if (destinationValue == 0) destinationValue = input.maxOrNull()!!
            destinationIndex = input.indexOf(destinationValue)
//            print(" destination $destinationIndex")
        } while (destinationIndex == -1)
//        println("destination index: $destinationIndex value: $destinationValue")

        input.addAll(destinationIndex + 1, removed)
        i = input.indexOf(currentValue)
        i = ((i + 1) % input.size)

//
//        println(" done turn $turn")
        if (turn % 100 == 0) {
            val one = input.indexOf(1)
            val two = input[(one + 1) % input.size]
            val three = input[(one + 2) % input.size]
            val result = two * three
            println(
                "turn $turn 1 is at ${one}, $two x $three  : list is now ${input.subList(0, 20)}...${
                    input.subList(
                        Math.max(0, one - 10),
                        Math.min(input.size, one + 10)
                    )
                }...${input.subList(input.size - 20, input.size)}"
            )
        }
    }

//    println("cups $input")

    val one = input.indexOf(1)
    val two = input[(one + 1) % input.size]
    val three = input[(one + 2) % input.size]
    val result = two * three

//
//    var j = one
//    println("one $one")
//    var result = ""
//    while (result.length < input.size - 1) {
//        j++
//        var j = j % input.size
//        result += input[j]
//
////        println("$result")
//    }
    println("result: $result")

}

fun printCups(cups: Array<Int?>, currentIndex: Int) {
    cups.forEachIndexed {index, i ->
        val s = when (currentIndex) {
            index -> " ($i) "
            else -> " $i "
        }
        print(s)
    }
    println("")
}
