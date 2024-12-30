import {
  cyanBright,
  gray,
  greenBG,
  redBright,
  yellow,
  yellowBG,
} from "console-log-colors";
import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import {
  CardinalDirection,
  oppositeDirection,
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
  return current.dir === next.dir ? 1 : 1000;
}

function solve(
  start: Node,
  //   finish: Point,
  maze: Grid<string>
): { distances: Map<string, number>; prev: Map<string, string> } {
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

    // if (u.p.equals(finish)) {
    //   // found the finish node
    //   //   return minDist;
    //   finishNode = u;
    //   break;
    // }

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

  return { distances: dist, prev: prev };
}

function buildPath(finish: Node, prev: Map<string, string>): Array<Node> {
  const path = new Array<Node>();
  let k = finish.key;
  path.push(finish);
  while (prev.has(k)) {
    k = prev.get(k);
    path.push(parseKey(k!));
  }
  path.reverse();
  return path;
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

function seatsOverlay(seats: Set<string>) {
  const overlay = new Map<string, string>();
  seats.forEach((seat) => {
    overlay.set(seat, "O");
  });
  return overlay;
}

const styles = new Map([
  ["S", redBright],
  ["E", redBright],
  ["^", cyanBright],
  ["v", cyanBright],
  [">", cyanBright],
  ["<", cyanBright],
  ["O", yellowBG],
  [".", gray],
]);

function findPathWithLowestScore(
  start: Node,
  finish: Point,
  distances: Map<string, number>,
  prev: Map<string, string>
): { minScore: number; path: Array<Node> } {
  // look at approaches to finish from different directions to find the
  // one with the lowest score
  let min = Infinity;
  let minFinish: Node;
  [
    CardinalDirection.N,
    CardinalDirection.S,
    CardinalDirection.E,
    CardinalDirection.W,
  ].forEach((dir) => {
    const finishNode: Node = { p: finish, dir: dir, key: key(finish, dir) };
    const dist = distances.get(finishNode.key);
    if (dist && dist < min) {
      min = dist;
      minFinish = finishNode;
    }
  });

  const path = buildPath(minFinish!, prev);
  // maze.log(styles, pathOverlay(path));
  // console.log(`lowest: ${min}`);
  return { minScore: min, path: path };
}

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
  const solution = solve(startNode, maze);
  const { distances, prev } = solution;

  // look at approaches to finish from different directions to find the
  // one with the lowest score
  const { minScore, path } = findPathWithLowestScore(
    startNode,
    finish,
    distances,
    prev
  );
  maze.log(styles, pathOverlay(path));
  console.log(`lowest: ${minScore}`);
}

function part2() {
  const maze = linesToCharGrid(lines);
  const start = maze.find(START);
  const finish = maze.find(END);

  maze.log(styles);

  // build paths from start to finish
  const startNode: Node = {
    p: start,
    dir: CardinalDirection.E,
    key: key(start, CardinalDirection.E),
  };

  console.log("calculating distances from start");
  const { distances: distancesFromStart, prev: prevFromStart } = solve(
    startNode,
    maze
  );

  // build paths from finish, with each direction, back to start
  const allDistancesFromFinish = new Array<Map<string, number>>();
  const allPrevsFromFinish = new Array<Map<string, string>>();
  const allFinishNodes = new Array<Node>();
  [
    CardinalDirection.N,
    CardinalDirection.S,
    CardinalDirection.E,
    CardinalDirection.W,
  ].forEach((dir) => {
    console.log(`calculating distances from finish ${dir}`);
    const finishNode: Node = { p: finish, dir: dir, key: key(finish, dir) };
    allFinishNodes.push(finishNode);
    const { distances: distancesFromFinish, prev: prevFromFinish } = solve(
      finishNode,
      maze
    );
    allDistancesFromFinish.push(distancesFromFinish);
    allPrevsFromFinish.push(prevFromFinish);
  });

  // for every node not already covered, see if the sum of the shortest path
  // from start to that node + the path from finish to that node is the same
  // as the shortest distance from start to finish.
  // look at approaches to finish from different directions to find the
  // one with the lowest score
  const { minScore, path: minScorePath } = findPathWithLowestScore(
    startNode,
    finish,
    distancesFromStart,
    prevFromStart
  );

  console.log(`min score is ${minScore}`);

  const seats = new Set<string>();
  minScorePath.forEach((node) => {
    seats.add(node.p.toString());
  });

  console.log(`checking all nodes`);
  const checkpoint = new Point(11, 13);

  for (let y = 0; y < maze.grid.length; y++) {
    for (let x = 0; x < maze.grid[y].length; x++) {
      const point = new Point(x, y);
      if (seats.has(point.toString())) continue;

      const value = maze.getValue(point);
      if (value != WALL) {
        if (point.equals(checkpoint)) {
          console.log(`checking ${point}: ${value}`);
        }
        const { minScore: distFromStart, path: pathFromStart } =
          findPathWithLowestScore(
            startNode,
            point,
            distancesFromStart,
            prevFromStart
          );

        // use the path to find the direction we are going when we
        // get to the point, to make its Node
        const pointNode = pathFromStart[pathFromStart.length - 1];
        const remainingDistance = minScore - distFromStart;

        if (point.equals(checkpoint)) {
          console.log(
            `${pointNode.key} is ${distFromStart} from start, ${remainingDistance} remaining`
          );
        }

        // then see if there is a path from the finish to the node that
        // covers the remaining distance.
        for (let i = 0; i < allDistancesFromFinish.length; i++) {
          const { minScore: distFromFinish, path: pathFromFinish } =
            findPathWithLowestScore(
              allFinishNodes[i],
              point,
              allDistancesFromFinish[i],
              allPrevsFromFinish[i]
            );
          const pointNodeFromFinish = pathFromFinish[pathFromFinish.length - 1];
          if (point.equals(checkpoint)) {
            console.log(
              `${point} is ${distFromFinish} from finish, with key ${pointNodeFromFinish.key}`
            );
          }

          let adjust = 0;
          if (pointNode.dir !== oppositeDirection(pointNodeFromFinish.dir)) {
            adjust = 1000;
            if (point.equals(checkpoint)) {
              console.log(
                `Adjusting +1000 for ${pointNode.dir} vs ${pointNodeFromFinish.dir}`
              );
            }
          }

          if (distFromFinish + adjust === remainingDistance) {
            if (point.equals(checkpoint)) {
              console.log(`adding seats from path `);
            }
            pathFromFinish.forEach((node) => {
              seats.add(node.p.toString());
            });
            pathFromStart.forEach((node) => {
              seats.add(node.p.toString());
            });
          }
        }
      }
    }
  }

  // maze.log(styles, seatsOverlay(seats));
  console.log(`Found seats: ${seats.size}`);
}

console.time();
part2();
console.timeEnd();
