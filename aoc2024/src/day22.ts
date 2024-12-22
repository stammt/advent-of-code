import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day22", true);

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

function getPrice(secretNumber: bigint): number {
  // blah
  const str = `${secretNumber}`;
  return parseInt(str.substring(str.length - 1));
}
function getPrices(secretNumber: bigint): number[] {
  const results: number[] = [];
  results.push(getPrice(secretNumber));
  const iterations = 2000;

  let s = secretNumber;
  for (let i = 0; i < iterations - 1; i++) {
    s = nextSecretNumber(s);
    results.push(getPrice(s));
  }
  return results;
}

function getPriceDiffs(prices: number[]): number[] {
  const results: number[] = [];

  for (let i = 1; i < prices.length; i++) {
    results.push(prices[i] - prices[i - 1]);
  }

  return results;
}

function part2() {
  lines.forEach((line) => {
    const s = BigInt(line);
    const prices = getPrices(s);
    const priceDiffs = getPriceDiffs(prices);
    for (let i = 0; i < prices.length; i++) {
      const diff = i > 0 ? `${priceDiffs[i - 1]}` : "";
      console.log(`${prices[i]} : ${diff}`);
    }
  });
}

part2();
