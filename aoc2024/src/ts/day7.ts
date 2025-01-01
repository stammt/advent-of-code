import { time, timeEnd, timeLog } from "console";
import { readInput } from "./utils/file-utils";
import { combinations } from "./utils/utils";

const lines = readInput("day7", false);

function evaluate(numbers: number[], ops: string[]): bigint {
  let acc = BigInt(numbers[0]);
  for (let i = 1; i < numbers.length; i++) {
    const op = ops[i - 1];
    const num = BigInt(numbers[i]);
    if (op === "+") {
      acc = acc + num;
    } else if (op === "*") {
      acc = acc * num;
    } else if (op === "||") {
      const s = `${acc}${num}`;
      acc = BigInt(s);
    }
  }
  return acc;
}

function part1() {
  let sum = BigInt(0);
  lines.forEach((line) => {
    const [testValue, numbersString] = line.split(":").map((e) => e.trim());
    const numbers = numbersString.split(" ").map((e) => parseInt(e.trim()));
    const opPermutations = combinations(["+", "*"], numbers.length - 1);
    console.log(`${testValue} from ${numbers} - ${opPermutations}`);

    for (let i = 0; i < opPermutations.length; i++) {
      const result = evaluate(numbers, opPermutations[i]);
      if (result === BigInt(testValue)) {
        console.log(`success with ${opPermutations[i]}`);
        sum = sum + result;
        break;
      }
    }
  });

  console.log(`sum: ${sum}`);
}

function part2() {
  let sum = BigInt(0);
  lines.forEach((line) => {
    const [testValue, numbersString] = line.split(":").map((e) => e.trim());
    const numbers = numbersString.split(" ").map((e) => parseInt(e.trim()));
    const opPermutations = combinations(["+", "*", "||"], numbers.length - 1);
    // console.log(`${testValue} from ${numbers} - ${opPermutations.join(" ")}`);

    for (let i = 0; i < opPermutations.length; i++) {
      const result = evaluate(numbers, opPermutations[i]);
      if (result === BigInt(testValue)) {
        // console.log(`success with ${opPermutations[i]}`);
        sum = sum + result;
        break;
      }
    }
  });

  console.log(`sum: ${sum}`);
}

time();
part2();
timeEnd();
