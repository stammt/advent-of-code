import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day22", false);

function mix(n: bigint, secretNumber: bigint): bigint {
  return n ^ secretNumber;
}

function prune(secretNumber: bigint): bigint {
  return secretNumber % 16777216n;
}

function nextSecretNumber(secretNumber: bigint): bigint {
  let step1 = secretNumber * 64n;
  step1 = prune(mix(step1, secretNumber));

  const step2 = prune(mix(step1 / 32n, step1));

  const step3 = prune(mix(step2 * 2048n, step2));

  return step3;
}

function part1() {
  let sum = 0n;
  lines.forEach((line) => {
    let s = BigInt(line);
    for (let i = 0; i < 2000; i++) {
      s = nextSecretNumber(s);
    }
    sum += s;
    console.log(`${line} : ${s}`);
  });

  console.log(`sum: ${sum}`);
}

function part2() {}

part1();
