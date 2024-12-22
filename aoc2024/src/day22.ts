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
  const prices: number[][] = [];
  const priceDiffs: number[][] = [];
  lines.forEach((line) => {
    const s = BigInt(line);
    const currentPrices = getPrices(s);
    const currentPriceDiffs = getPriceDiffs(currentPrices);
    prices.push(currentPrices);
    priceDiffs.push(currentPriceDiffs);
  });

  // for each buyer, build a map of sequence to price (where sequence is a string representation)
  // then get the union of all sequences and check the sum across buyers
  const sequenceToPriceMap = new Array<Map<string, number>>();
  const allSequences = new Set<string>();
  for (let buyer = 0; buyer < prices.length; buyer++) {
    const currentPrices = prices[buyer];
    const currentPriceDiffs = priceDiffs[buyer];
    const map = new Map<string, number>();
    for (let start = 0; start < currentPriceDiffs.length - 5; start++) {
      const sequence = currentPriceDiffs.slice(start, start + 4).join();
      const value = currentPrices[start + 4];
      if (!map.has(sequence)) {
        map.set(sequence, value);
        allSequences.add(sequence);
      }
    }
    sequenceToPriceMap.push(map);
  }

  let bestSequence: string = "";
  let bestSequencePrice: number = -Infinity;
  allSequences.forEach((sequence) => {
    let sum = 0;
    for (let i = 0; i < sequenceToPriceMap.length; i++) {
      const price = sequenceToPriceMap[i].get(sequence);
      if (price) {
        sum += price;
      }
    }
    if (sum > bestSequencePrice) {
      bestSequence = sequence;
      bestSequencePrice = sum;
    }
  });

  console.log(`best ${bestSequence} gets ${bestSequencePrice}`);
}

part2();
