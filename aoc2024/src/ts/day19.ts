import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day19", false);

function isPossible(design: string, towels: string[]): boolean {
  const candidates = towels.filter((t) => design.startsWith(t));
  for (let i = 0; i < candidates.length; i++) {
    const t = candidates[i];
    if (design.length === t.length) {
      return true;
    }
    if (isPossible(design.slice(t.length), towels)) {
      return true;
    }
  }
  return false;
}

const cache = new Map<string, number>();

function getArrangementCount(design: string, towels: string[]): number {
  if (cache.has(design)) {
    // console.log(`cache hit for ${design}`);
    return cache.get(design)!;
  }

  const candidates = towels.filter((t) => design.startsWith(t));
  let results = 0;
  //   console.log(`${design} : checking ${candidates}`);
  for (let i = 0; i < candidates.length; i++) {
    const t = candidates[i];
    if (design.length === t.length) {
      results += 1;
    } else {
      const a = getArrangementCount(design.slice(t.length), towels);
      results += a;
    }
  }

  cache.set(design, results);
  return results;
}

function part1() {
  const towels = lines[0].split(", ");
  const designs = lines.slice(2);

  let count = 0;
  designs.forEach((design) => {
    if (isPossible(design, towels)) {
      count += 1;
    }
  });

  console.log(`Count ${count}`);
}

function part2() {
  const towels = lines[0].split(", ");
  const designs = lines.slice(2);

  let count = 0;
  designs.forEach((design) => {
    const a = getArrangementCount(design, towels);
    console.log(`*** ${design} : ${a}\n`);
    count += a;
  });

  console.log(`Count ${count}`);
}

part2();
