import { cyanBright, gray, greenBG, redBright } from "console-log-colors";
import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import {
  CardinalDirection,
  parseDirection,
  parsePoint,
  Point,
} from "./utils/point";

const lines = readInput("day16", false);

const START = "S";
const WALL = "#";
const END = "E";

// each node is a point in the maze + direction, so turning
// moves to a new node even though the maze position is the
// same
type Node = {
  p: Point;
  dir: CardinalDirection;
};

function key(n: Node): string {
  return `${n.p}:${n.dir}`;
}
function parseKey(key: string): Node {
  const [pString, dirString] = key.split(":");
  return {
    p: parsePoint(pString),
    dir: parseDirection(dirString)!,
  };
}

function neighborNodes(n: Node): Node[] {
  const results = new Array<Node>();

  // All turns in the current position.
  [
    CardinalDirection.N,
    CardinalDirection.E,
    CardinalDirection.S,
    CardinalDirection.W,
  ].forEach((dir) => {
    if (dir !== n.dir) {
      results.push({ p: n.p, dir: dir });
    }
  });

  // The next node in the current direction.
  results.push({ p: n.p.step(n.dir), dir: n.dir });

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
): number | undefined {
  const dist = new Map<string, number>();
  const prev = new Map<string, string>();
  const q = new Set<string>();

  maze.iterate((x, y, s) => {
    if (s !== WALL) {
      const point = new Point(x, y);
      q.add(
        key({
          p: point,
          dir: CardinalDirection.N,
        })
      );
      q.add(
        key({
          p: point,
          dir: CardinalDirection.S,
        })
      );
      q.add(
        key({
          p: point,
          dir: CardinalDirection.E,
        })
      );
      q.add(
        key({
          p: point,
          dir: CardinalDirection.W,
        })
      );
    }
  });

  dist.set(key(start), 0);

  while (q.size > 0) {
    // find the node with min distance
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
      return minDist;
    }

    const neighbors = neighborNodes(u).filter((n) => q.has(key(n)));
    // console.log(
    //   `${uKey} has ${neighbors.length} neighbors: ${neighbors.map((e) => key(e))}`
    // );
    for (let i = 0; i < neighbors.length; i++) {
      const nKey = key(neighbors[i]);
      const alt = minDist + score(u, neighbors[i]);
      if (!dist.has(nKey) || alt < dist.get(nKey)!) {
        dist.set(nKey, alt);
        prev.set(nKey, uKey!);
      }
    }
  }

  return undefined;
}

function validNextSteps(
  n: Node,
  maze: Grid<string>,
  visited: Set<string>
): Node[] {
  const results = new Array<Node>();

  function addIfNotVisited(next: Node) {
    if (!visited.has(key(next))) {
      results.push(next);
    }
  }

  // All turns in the current position.
  if (n.dir === CardinalDirection.N || n.dir === CardinalDirection.S) {
    addIfNotVisited({ p: n.p, dir: CardinalDirection.E });
    addIfNotVisited({ p: n.p, dir: CardinalDirection.W });
  } else {
    addIfNotVisited({ p: n.p, dir: CardinalDirection.N });
    addIfNotVisited({ p: n.p, dir: CardinalDirection.S });
  }

  // The next node in the current direction.
  const next: Node = { p: n.p.step(n.dir), dir: n.dir };
  if (maze.getValue(next.p) !== WALL) {
    addIfNotVisited(next);
  }

  console.log(`from ${key(n)} could go ${results.map((e) => key(e))}`);
  return results;
}

type Path = {
  nodes: Node[];
  score: number;
};

function findAllPaths(
  pathSoFar: Path,
  finish: Point,
  maze: Grid<string>,
  visited: string[]
): Path[] {
  const results = new Array<Path>();
  const node = pathSoFar.nodes[pathSoFar.nodes.length - 1];

  const nextSteps = new Array<Node>();
  const dirs =
    node.dir === CardinalDirection.N || node.dir === CardinalDirection.S
      ? [node.dir, CardinalDirection.E, CardinalDirection.W]
      : [node.dir, CardinalDirection.N, CardinalDirection.S];
  dirs.forEach((dir) => {
    const step = { p: node.p.step(dir), dir: dir };
    if (maze.getValue(step.p) !== WALL && !visited.includes(key(step))) {
      nextSteps.push(step);
    }
  });

  //   console.log(`from ${key(node)} could go ${nextSteps.map((e) => key(e))}`);

  //   const nextSteps = validNextSteps(node, maze, visited);

  //   if (node.p.x === 3 && node.p.y === 7) {
  //     console.log(
  //       `at 3,7 ${node.dir} considering next steps ${nextSteps.map((e) => key(e))}`
  //     );
  //   }
  for (let i = 0; i < nextSteps.length; i++) {
    const score = 1 + (nextSteps[i].dir !== node.dir ? 1000 : 0);
    const pathWithStep: Path = {
      nodes: pathSoFar.nodes.concat(nextSteps[i]),
      score: pathSoFar.score + score,
    };

    if (nextSteps[i].p.equals(finish)) {
      console.log(`Found the finish with score ${pathWithStep.score}`);
      results.push(pathWithStep);
    } else {
      //   visited.add(key(nextSteps[i]));
      const v = visited.concat([key(nextSteps[i])]);
      const p = findAllPaths(pathWithStep, finish, maze, v);
      results.push(...p);
    }
  }
  return results;
}

function allPaths(start: Node, finish: Point, maze: Grid<string>): Path[] {
  return findAllPaths({ nodes: [start], score: 0 }, finish, maze, [key(start)]);
}

function pathOverlay(path: Path) {
  const overlay = new Map<string, string>();
  for (let i = 0; i < path.nodes.length; i++) {
    const n = path.nodes[i];
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
  };

  // just need to find the lowest score
  const score = solve(startNode, finish, maze);

  console.log(`lowest: ${score}`);
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
  const paths = allPaths(startNode, finish, maze);
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
      path.nodes.forEach((node) => {
        seats.add(node.p.toString());
      });
    }
  });

  console.log(`lowest: ${minScore}, with ${seats.size} seats`);
}

part2();
