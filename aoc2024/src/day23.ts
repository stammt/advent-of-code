import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";
import { allPairs, getSubsets } from "./utils/utils";

const lines = readInput("day23", false);

function buildConnectionMap(lines: string[]): Map<string, string[]> {
  const connections = new Map<string, string[]>();
  lines.forEach((line) => {
    const [c1, c2] = line.split("-");
    if (connections.has(c1)) {
      connections.get(c1)?.push(c2);
    } else {
      connections.set(c1, [c2]);
    }
    if (connections.has(c2)) {
      connections.get(c2)?.push(c1);
    } else {
      connections.set(c2, [c1]);
    }
  });
  return connections;
}

function getComputers(lines: string[]): Set<string> {
  const results = new Set<string>();
  lines.forEach((line) => {
    const [c1, c2] = line.split("-");
    results.add(c1);
    results.add(c2);
  });
  return results;
}

function isConnected(
  c1: string,
  c2: string,
  connections: Map<string, string[]>
): boolean {
  return connections.has(c1) && connections.get(c1)!.includes(c2);
}

function areAllConnected(
  computers: string[],
  connections: Map<string, string[]>
): boolean {
  for (let x = 0; x < computers.length; x++) {
    const c = computers[x];
    for (let y = 0; y < computers.length; y++) {
      if (x !== y && !isConnected(c, computers[y], connections)) return false;
    }
  }
  return true;
}

function part1() {
  const connections = buildConnectionMap(lines);
  const computers = getComputers(lines);

  const clusters = new Set<string>();
  computers.forEach((c1) => {
    const c2Array = connections.get(c1);
    if (c2Array) {
      const pairs = allPairs(c2Array);
      pairs.forEach((pair) => {
        if (
          c1.startsWith("t") ||
          pair.a.startsWith("t") ||
          pair.b.startsWith("t")
        ) {
          if (isConnected(pair.a, pair.b, connections)) {
            clusters.add(`${[c1, pair.a, pair.b].sort()}`);
          }
        }
      });
    }
  });
  console.log(clusters.size);
  clusters.forEach((cluster) => {
    console.log(cluster);
  });
}

function part2() {
  const connections = buildConnectionMap(lines);
  const computers = getComputers(lines);

  const clusters = new Set<string>();
  computers.forEach((c1) => {
    // find all subsets of c1's connections that are all connected to each other
    const c2Array = connections.get(c1)!;
    const subsets = getSubsets(c2Array).filter((e) => e.length > 0);

    subsets.forEach((candidate) => {
      if (areAllConnected(candidate, connections)) {
        clusters.add(`${[c1, ...candidate].sort()}`);
      }
    });
  });
  console.log(clusters.size);
  let longest = "";
  clusters.forEach((cluster) => {
    if (cluster.length > longest.length) {
      longest = cluster;
    }
  });
  console.log(longest);
}

part2();
