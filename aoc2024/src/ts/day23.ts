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

// 2.8s
function part2_first() {
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

// 950ms
function part2_second() {
  const connections = buildConnectionMap(lines);
  const computers = getComputers(lines);

  const clusters = new Set<string>();
  computers.forEach((c1) => {
    // find all subsets of c1's connections that are all connected to each other
    const c2Array = connections.get(c1)!;
    const subsets = getSubsets(c2Array).filter((e) => e.length > 0);
    subsets.sort((a, b) => a.length - b.length);

    // Sort by subset size, and stop when we find one that's all connected
    for (let i = subsets.length - 1; i--; i > 0) {
      const candidate = subsets[i];
      if (areAllConnected(candidate, connections)) {
        clusters.add(`${[c1, ...candidate].sort()}`);
        break;
      }
    }
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

function expandClique(
  computer: string,
  click: Set<string>,
  connections: Map<string, string[]>
): Set<string> {
  click.add(computer);

  connections.get(computer)!.forEach((c2) => {
    if (!click.has(c2)) {
      const c2Connections = connections.get(c2)!;
      // click is a subset of c2Connections
      if (isSubset(click, c2Connections)) {
        expandClique(c2, click, connections);
      }
    }
  });
  return click;
}

function isSubset(a: Set<string>, b: Array<string>): boolean {
  const aa = Array.from(a);
  for (let i = 0; i < aa.length; i++) {
    if (!b.includes(aa[i])) return false;
  }
  return true;
}

// 12ms
function part2() {
  const connections = buildConnectionMap(lines);
  const computers = getComputers(lines);

  const clusters = new Array<Set<string>>();
  computers.forEach((c1) => {
    const click = expandClique(c1, new Set<string>(), connections);
    clusters.push(click);
  });
  console.log(clusters.length);
  let longest: Set<string> = new Set<string>();
  clusters.forEach((cluster) => {
    if (cluster.size > longest.size) {
      longest = cluster;
    }
  });
  const final = Array.from(longest);
  final.sort();
  console.log(`${final.join(",")}`);
}

console.time();
part2();
console.timeEnd();
