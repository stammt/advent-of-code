import java.io.File

fun main(args: Array<String>) {
    val input = File("/Users/stammt/dev/aoc/day21input.txt").readLines()

//    val input = listOf( "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
//            "trh fvjkl sbzzf mxmxvkd (contains dairy)",
//            "sqjhc fvjkl (contains soy)",
//            "sqjhc mxmxvkd sbzzf (contains fish)")

    //    val input = listOf( "mxmxvkd  sqjhc  (contains dairy, fish)",
//            " fvjkl  mxmxvkd (contains dairy)",
//            "sqjhc fvjkl (contains soy)",
//            "sqjhc mxmxvkd  (contains fish)")

    day21Part1(input)
}

class Food(val ingredients: List<String>, val allergens: List<String>) {
    fun containsAllergen(allergen: String) : Boolean {
        return allergens.contains(allergen)
    }

    fun containsIngredient(ingredient: String) : Boolean {
        return ingredients.contains(ingredient)
    }
}

fun day21Part1(input: List<String>) {
    val foods = mutableListOf<Food>()
    val ingredients = mutableSetOf<String>()
    val allergens = mutableSetOf<String>()
    val ingredientCounts = mutableMapOf<String, Int>()

    input.forEach {
        val parts = it.trim().split("(contains ")
        val ingredientList = parts[0].trim().split(" ")
        val i = mutableListOf<String>()
        ingredientList.forEach{

            ingredients.add(it.trim())
            i.add(it.trim())
            val oldCount = ingredientCounts[it.trim()] ?: 0
            ingredientCounts[it.trim()] = oldCount + 1
        }
        val a = mutableListOf<String>()
        if (parts.size == 2) {
            val p1 = parts[1].trim()
            val allergenList = p1.substring(0, p1.length - 1).split(", ")
            allergenList.forEach{
                allergens.add(it.trim())
                a.add(it.trim())
            }
        }
        foods.add(Food(i, a))
    }

    println("allergens: $allergens")
    println("ingredients: $ingredients")

    // for each allergen, remove ingredients that are in all foods containing that
    // allergen
    val candidateSafeIngredients = ingredients.toMutableSet()
    val foodsContainingAllergen = mutableMapOf<String, List<Food>>()
    allergens.forEach {a ->
        val allFoods = mutableListOf<Food>()
        foods.forEach {f ->
            if (f.containsAllergen(a)) {
                allFoods.add(f)
            }
        }
        foodsContainingAllergen[a] = allFoods

        candidateSafeIngredients.removeAll { i -> allFoods.all { it.containsIngredient(i)} }
    }

    println("safe: $candidateSafeIngredients")

    var count = 0
    candidateSafeIngredients.forEach {
        count += ingredientCounts[it]!!
    }
    println("safe count: $count")


    // each unsafe ingredient has exactly one allergen
    // build a list of potential allergens for each ingredient, then iterate
    // and use a process of elimination by removing the ones with one
    // potential allergen, then removing that allergen from the others,
    // until we narrow down which ingredient has which allergen
    val unsafeIngredients = ingredients.toMutableSet()
    unsafeIngredients.removeAll(candidateSafeIngredients)

    val potentialAllergens = mutableMapOf<String, MutableList<String>>()
    unsafeIngredients.forEach{ i ->
        val list = mutableListOf<String>()
        foodsContainingAllergen.forEach {
            val foodsWithThisAllergen = it.value
            if (foodsWithThisAllergen.all { f -> f.containsIngredient(i) }) {
                list.add(it.key)
            }
        }
        potentialAllergens[i] = list
    }

    val definiteAllergens = mutableMapOf<String, String>()
    val potentialCount = potentialAllergens.size
    while (potentialAllergens.isNotEmpty()) {
        var foundIngredient: String? = null
        var foundAllergen: String? = null
        potentialAllergens.forEach {
            if (it.value.size == 1) {
                foundIngredient = it.key
                foundAllergen = it.value[0]
            }
        }
        if (foundIngredient == null || foundAllergen == null) {
            break
        }
        potentialAllergens.remove(foundIngredient)
        definiteAllergens[foundAllergen!!] = foundIngredient!!

        potentialAllergens.forEach {e ->
            e.value.remove(foundAllergen)
        }
    }

    println("Potentials: $potentialCount Definites: ${definiteAllergens}")

    val sortedIngredients = mutableListOf<String>()
    allergens.sorted().forEach {
        definiteAllergens[it]?.let { it1 -> sortedIngredients.add(it1) }
    }
    println("part 2: ${sortedIngredients.joinToString(",")}")

}

