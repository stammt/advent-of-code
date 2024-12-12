import { Grid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day11", false);

function part1() {
  let stones = lines[0].split(" ").map((e) => BigInt(e));
  console.log(`Initial: ${stones}`);

  for (let i = 0; i < 25; i++) {
    const updatedStones = new Array<bigint>();
    for (let j = 0; j < stones.length; j++) {
      if (stones[j] === BigInt(0)) {
        updatedStones.push(BigInt(1));
      } else {
        const s = `${stones[j]}`;
        if (s.length % 2 === 0) {
          const s1 = s.substring(0, s.length / 2);
          const s2 = s.substring(s.length / 2);
          updatedStones.push(BigInt(s1));
          updatedStones.push(BigInt(s2));
        } else {
          updatedStones.push(stones[j] * BigInt(2024));
        }
      }
    }
    stones = updatedStones;
    console.log(`*** Round ${i} done: ${stones.length}`);
  }
  console.log(`Stone count: ${stones.length}`);
}

// DFS step through each entry in the list, caching the result of expanding an
// entry for each number of steps.
function blinkRecursive(
  value: bigint,
  steps: number,
  counts: Map<string, number>
): number {
  if (steps === 0) {
    return 1;
  }

  const key = `${value}:${steps}`;
  if (counts.has(key)) {
    // console.log(`Found ${key}`);
    return counts.get(key)!;
  }

  if (value === BigInt(0)) {
    const count = blinkRecursive(BigInt(1), steps - 1, counts);
    counts.set(key, count);
    return count;
  } else {
    const s = `${value}`;
    if (s.length % 2 === 0) {
      const s1 = s.substring(0, s.length / 2);
      const s2 = s.substring(s.length / 2);
      const v1 = BigInt(s1);
      const v2 = BigInt(s2);
      const count1 = blinkRecursive(v1, steps - 1, counts);
      const count2 = blinkRecursive(v2, steps - 1, counts);
      counts.set(key, count1 + count2);
      return count1 + count2;
    } else {
      const v = value * BigInt(2024);
      const count = blinkRecursive(v, steps - 1, counts);
      counts.set(key, count);
      return count;
    }
  }
}

function part2() {
  const steps = 75;

  const stones = lines[0].split(" ").map((e) => {
    return BigInt(e);
  });
  console.log(`Initial: ${stones}`);

  // Track what each number will transform to
  const counts = new Map<string, number>();

  let sum = 0;
  for (let i = 0; i < stones.length; i++) {
    const count = blinkRecursive(stones[i], steps, counts);
    sum += count;
  }
  console.log(`sum total: ${sum}`);
}

part2();
