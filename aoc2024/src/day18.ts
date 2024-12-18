import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point, parsePoint } from "./utils/point";

const lines = readInput("day18", false);

const CORRUPTED = "#";

function isInGrid(p: Point, gridSize: number): boolean {
  return p.x >= 0 && p.x < gridSize && p.y >= 0 && p.y < gridSize;
}

function neighborPoints(p: Point, gridSize: number): Point[] {
  const results = new Array<Point>();
  [
    CardinalDirection.N,
    CardinalDirection.S,
    CardinalDirection.E,
    CardinalDirection.W,
  ].forEach((dir) => {
    const n = p.step(dir);
    if (isInGrid(n, gridSize)) results.push(n);
  });
  return results;
}

function solve(
  start: Point,
  finish: Point,
  gridSize: number,
  corrupted: string[]
): { distances: Map<string, number>; prev: Map<string, string> } {
  const dist = new Map<string, number>();
  const prev = new Map<string, string>();
  const q = new Set<string>();

  //   console.log(corrupted);

  // Add all non-corrupted nodes.
  for (let x = 0; x < gridSize; x++) {
    for (let y = 0; y < gridSize; y++) {
      const p = new Point(x, y);
      if (!corrupted.includes(p.toString())) {
        q.add(p.toString());
      }
    }
  }

  //   console.log(q);
  dist.set(start.toString(), 0);

  while (q.size > 0) {
    // find the node in the q with min distance
    let uKey: string;
    let minDist = Infinity;
    dist.forEach((d, key) => {
      if (q.has(key)) {
        if (d < minDist) {
          uKey = key;
          minDist = d;
        }
      }
    });
    // console.log(`looking at ${uKey} with dist ${minDist}`);
    if (!uKey) {
      // just return what we have, the finish point won't be in there.
      return { prev: prev, distances: dist };
    }
    q.delete(uKey!);
    const u = parsePoint(uKey!);

    if (u.equals(finish)) {
      // found the finish node
      return { prev: prev, distances: dist };
    }

    const neighbors = neighborPoints(u, gridSize).filter((n) =>
      q.has(n.toString())
    );

    // console.log(`${uKey} has ${neighbors.length} neighbors: ${neighbors}`);
    for (let i = 0; i < neighbors.length; i++) {
      const nKey = neighbors[i].toString();
      const alt = minDist + 1;
      if (!dist.has(nKey) || alt < dist.get(nKey)!) {
        dist.set(nKey, alt);
        prev.set(nKey, uKey!);
      }
    }
  }

  return { distances: dist, prev: prev };
}

function getBestPath(
  finish: Point,
  prev: Map<string, string>
): Array<string> | undefined {
  const path = new Array<string>();
  let p = finish.toString();
  if (!prev.has(p)) return undefined;

  while (prev.has(p)) {
    path.push(p);
    p = prev.get(p);
  }
  return path;
}

function part1() {
  const fallen = lines; //.map((e) => parsePoint(e));

  //   const gridSize = 7; // 0-6
  //   const fallCount = 12;

  const gridSize = 71; // 0-70
  const fallCount = 1024;

  const finish = new Point(gridSize - 1, gridSize - 1);

  const { prev, distances } = solve(
    new Point(0, 0),
    finish,
    gridSize,
    fallen.slice(0, fallCount)
  );
  const steps = distances.get(finish.toString());
  console.log(`steps: ${steps}`);
}

function part2() {
  //   const gridSize = 7; // 0-6
  //   const fallCount = 12;

  const gridSize = 71; // 0-70
  const fallCount = 1024;

  // Get the initial best path
  const finish = new Point(gridSize - 1, gridSize - 1);
  const fallen = lines.slice(0, fallCount);
  const { prev } = solve(new Point(0, 0), finish, gridSize, fallen);
  let bestPath = getBestPath(finish, prev);

  // For each next falling byte, if it doesn't fall on the best path, ignore it.
  // Otherwise re-calculate the next best path.
  let blocker: string;
  for (let i = fallCount; i < lines.length; i++) {
    const nextByte = lines[i];
    fallen.push(nextByte);
    console.log(`fall: ${nextByte}`);
    if (bestPath!.includes(nextByte)) {
      const { prev: updatedPrev } = solve(
        new Point(0, 0),
        finish,
        gridSize,
        fallen
      );
      bestPath = getBestPath(finish, updatedPrev);
      if (!bestPath) {
        blocker = lines[i];
        break;
      }
    }
  }
  console.log(`blocker: ${blocker}`);
}

part2();
