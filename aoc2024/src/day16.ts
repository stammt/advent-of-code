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

type Path = {
  //   nodes: Node[];
  lastNode: Node;
  score: number;
  visited: Array<string>;
};

function findAllPaths(start: Node, finish: Point, maze: Grid<string>): Path[] {
  let lowestScore = 107512; // we know this from part 1!

  const results = new Array<Path>();
  const q = new Queue<Path>();
  q.prepend({ lastNode: start, score: 0, visited: [key(start.p, start.dir)] });

  let i = 0;
  while (q.hasNext()) {
    i++;
    const pathSoFar = q.next();

    if (i % 100000 === 0) {
      console.log(`i is ${i} q size ${q.size}`);
    }

    // const node = pathSoFar.nodes[pathSoFar.nodes.length - 1];
    const node = pathSoFar.lastNode;

    const nextSteps = new Array<Node>();
    const dirs =
      node.dir === CardinalDirection.N || node.dir === CardinalDirection.S
        ? [node.dir, CardinalDirection.E, CardinalDirection.W]
        : [node.dir, CardinalDirection.N, CardinalDirection.S];
    dirs.forEach((dir) => {
      const stepPoint = node.p.step(dir);
      const stepKey = key(stepPoint, dir);
      const oppositeDir =
        dir == CardinalDirection.N
          ? CardinalDirection.S
          : dir === CardinalDirection.S
            ? CardinalDirection.N
            : dir === CardinalDirection.E
              ? CardinalDirection.W
              : CardinalDirection.E;
      const oppositeKey = key(stepPoint, oppositeDir);
      if (
        maze.getValue(stepPoint) !== WALL &&
        !pathSoFar.visited.includes(stepKey) &&
        !pathSoFar.visited.includes(oppositeKey)
      ) {
        const step = { p: stepPoint, dir: dir, key: stepKey };
        nextSteps.push(step);
      }
    });

    for (let ns = 0; ns < nextSteps.length; ns++) {
      const score = 1 + (nextSteps[ns].dir !== node.dir ? 1000 : 0);
      const pathWithStep: Path = {
        // nodes: pathSoFar.nodes.concat(nextSteps[ns]),
        lastNode: nextSteps[ns],
        score: pathSoFar.score + score,
        visited: pathSoFar.visited.concat([nextSteps[ns].key]),
      };

      if (nextSteps[ns].p.equals(finish)) {
        console.log(`Found the finish with score ${pathWithStep.score}`);
        results.push(pathWithStep);
        lowestScore = Math.min(pathWithStep.score, lowestScore);
      } else {
        // Only keep processing this path if it might be tied for lowest score.
        if (pathWithStep.score <= lowestScore) {
          q.prepend(pathWithStep);
          //   q.splice(i + 1, 0, pathWithStep);
          // } else {
          //   console.log(
          //     `cutting off path with score at least ${pathWithStep.score} > ${lowestScore}`
          //   );
        }
      }
    }
  }
  return results;
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

part2();
