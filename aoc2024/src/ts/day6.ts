import { readInput } from "./utils/file-utils";
import { Point, CardinalDirection, parsePoint } from "./utils/point";
import { isOnTheGrid } from "./utils/char-grid";

const lines = readInput("day6", false);

function getStart(): Point | undefined {
  for (let y = 0; y < lines.length; y++) {
    const x = lines[y].indexOf("^");
    if (x > 0) {
      return new Point(x, y);
    }
  }
  return undefined;
}

function getPointsOnPath(
  start: Point,
  obstacle?: Point
): { points: Set<string>; loop: boolean } {
  let p = start;
  let dir = CardinalDirection.N;
  const positions = new Set<string>();
  const path = new Array<string>();
  const posdirs = new Set<string>();
  let loop = false;
  while (true) {
    positions.add(p.toString());
    path.push(p.toString());
    posdirs.add(`${p.toString()}-${dir}`);
    const nextPoint = p.step(dir);
    if (!isOnTheGrid(nextPoint, lines)) {
      // console.log(
      //   `guard left the grid with ${obstacle}, path=${path.join(" ")}`
      // );
      break;
    }

    // It's a loop if we get back to a point and direction that we've already seen.
    // inefficient but it works :-/
    if (posdirs.has(`${nextPoint.toString()}-${dir}`)) {
      // console.log(
      //   `guard looped with ${obstacle}, path=${path.join(" ")}, ${p} and ${nextPoint}`
      // );
      loop = true;
      break;
    }

    const c = lines[nextPoint.y][nextPoint.x];
    if (c === "#" || nextPoint.equals(obstacle)) {
      // Don't move, just rotate
      if (dir === CardinalDirection.N) dir = CardinalDirection.E;
      else if (dir === CardinalDirection.E) dir = CardinalDirection.S;
      else if (dir === CardinalDirection.S) dir = CardinalDirection.W;
      else if (dir === CardinalDirection.W) dir = CardinalDirection.N;
    } else {
      p = nextPoint;
    }
  }
  return { points: positions, loop: loop };
}

function part1() {
  const start = getStart();
  const { points } = getPointsOnPath(start!);
  console.log(`positions size: ${points.size} `);
}

function part2() {
  const start = getStart()!;
  // const { points: basePoints } = getPointsOnPath(start);

  let count = 0;
  let i = 0;
  for (let y = 0; y < lines.length; y++) {
    for (let x = 0; x < lines[y].length; x++) {
      const p = new Point(x, y);
      console.log(`trying  ${i} : ${p}`);
      i++;
      if (!p.equals(start)) {
        const { loop } = getPointsOnPath(start, p);
        if (loop) {
          count++;
        }
      }
    }
  }

  console.log(`number of loops: ${count} `);
}

part2();
