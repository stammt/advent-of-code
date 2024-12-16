import { cyanBright, gray, greenBG, redBright } from "console-log-colors";
import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import {
  CardinalDirection,
  parseDirection,
  parsePoint,
  Point,
} from "./utils/point";
import { Queue } from "./utils/queue";

const lines = readInput("day16", true);

const START = "S";
const WALL = "#";
const END = "E";

// each node is a point in the maze + direction, so turning
// moves to a new node even though the maze position is the
// same
type Node = {
  p: Point;
  dir: CardinalDirection;
  key: string;
};

function key(p: Point, dir: CardinalDirection): string {
  return `${p}:${dir}`;
}
function parseKey(key: string): Node {
  const [pString, dirString] = key.split(":");
  return {
    p: parsePoint(pString),
    dir: parseDirection(dirString)!,
    key: key,
  };
}

function neighborNodes(n: Node): Node[] {
  const results = new Array<Node>();

  // All turns in the current position.
  const dirs =
    n.dir === CardinalDirection.N || n.dir === CardinalDirection.S
      ? [CardinalDirection.E, CardinalDirection.W]
      : [CardinalDirection.N, CardinalDirection.S];
  dirs.forEach((dir) => {
    // const s = n.p.step(dir);
    results.push({ p: n.p, dir: dir, key: key(n.p, dir) });
  });

  const s = n.p.step(n.dir);
  results.push({ p: s, dir: n.dir, key: key(s, n.dir) });

  return results;
}

function score(current: Node, next: Node) {
  let s = 0;
  if (current.dir != next.dir) {
    if (
      current.dir === CardinalDirection.N ||
      current.dir === CardinalDirection.S
    ) {
      s +=
        next.dir === CardinalDirection.E || CardinalDirection.W ? 1000 : 2000;
    } else if (
      current.dir === CardinalDirection.E ||
      current.dir === CardinalDirection.W
    ) {
      s +=
        next.dir === CardinalDirection.N || CardinalDirection.S ? 1000 : 2000;
    }
  } else {
    s = 1;
  }

  return s;
}

function solve(
  start: Node,
  finish: Point,
  maze: Grid<string>
): { score: number; path: Array<Node> } | undefined {
  const dist = new Map<string, number>();
  const prev = new Map<string, string>();
  const q = new Set<string>();

  // Add all non-wall nodes.
  maze.iterate((x, y, s) => {
    if (s !== WALL) {
      const point = new Point(x, y);
      q.add(key(point, CardinalDirection.N));
      q.add(key(point, CardinalDirection.S));
      q.add(key(point, CardinalDirection.E));
      q.add(key(point, CardinalDirection.W));
    }
  });

  dist.set(start.key, 0);
  let finishNode: Node;

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
    q.delete(uKey!);
    const u = parseKey(uKey!);

    if (u.p.equals(finish)) {
      // found the finish node
      //   return minDist;
      finishNode = u;
      break;
    }

    const neighbors = neighborNodes(u).filter((n) => q.has(n.key));
    // console.log(
    //   `${uKey} has ${neighbors.length} neighbors: ${neighbors.map((e) => key(e))}`
    // );
    for (let i = 0; i < neighbors.length; i++) {
      const nKey = neighbors[i].key;
      const alt = minDist + score(u, neighbors[i]);
      if (!dist.has(nKey) || alt < dist.get(nKey)!) {
        dist.set(nKey, alt);
        prev.set(nKey, uKey!);
      }
    }
  }

  // build the path
  if (finishNode) {
    const path = new Array<Node>();
    let k = finishNode.key;
    path.push(finishNode);
    while (prev.has(k)) {
      k = prev.get(k);
      path.push(parseKey(k!));
    }
    path.reverse();
    return { score: dist.get(finishNode.key)!, path: path };
  }
  return undefined;
}

function pathOverlay(path: Array<Node>) {
  const overlay = new Map<string, string>();
  for (let i = 0; i < path.length; i++) {
    const n = path[i];
    const key = n.p.toString();
    const ch =
      n.dir === CardinalDirection.N
        ? "^"
        : n.dir === CardinalDirection.S
          ? "v"
          : n.dir === CardinalDirection.E
            ? ">"
            : "<";
    overlay.set(key, ch);
  }
  return overlay;
}

const styles = new Map([
  ["S", redBright],
  ["E", redBright],
  ["^", cyanBright],
  ["v", cyanBright],
  [">", cyanBright],
  ["<", cyanBright],
  [".", gray],
]);

function part1() {
  const maze = linesToCharGrid(lines);
  const start = maze.find(START);
  const finish = maze.find(END);

  maze.log(styles);

  const startNode: Node = {
    p: start,
    dir: CardinalDirection.E,
    key: key(start, CardinalDirection.E),
  };

  // just need to find the lowest score
  const solution = solve(startNode, finish, maze);
  if (solution) {
    const { score, path } = solution;
    maze.log(styles, pathOverlay(path));
    console.log(`lowest: ${score}`);
  }
}

function part2() {
  const maze = linesToCharGrid(lines);
  const start = maze.find(START);
  const finish = maze.find(END);

  maze.log(styles);

  const startNode: Node = {
    p: start,
    dir: CardinalDirection.E,
  };

  // just need to find the lowest score
  const paths = findAllPaths(startNode, finish, maze);
  console.log(`Found ${paths.length} paths`);

  let minScore = Infinity;
  paths.forEach((path) => {
    // console.log(`score ${path.score}:`);
    // maze.log(styles, pathOverlay(path));
    if (path.score < minScore) {
      minScore = path.score;
    }
  });

  const seats = new Set<string>();
  paths.forEach((path) => {
    if (path.score === minScore) {
      path.visited.forEach((nodeKey) => {
        const node = parseKey(nodeKey);
        seats.add(node.p.toString());
      });
      //   path.nodes.forEach((node) => {
      //     seats.add(node.p.toString());
      //   });
    }
  });

  console.log(`lowest: ${minScore}, with ${seats.size} seats`);
}

part1();
