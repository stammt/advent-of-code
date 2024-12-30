import {
  Grid,
  linesToCharGrid,
  printSparseGrid,
  sparseGrid,
} from "./utils/char-grid";
import { greenBG, gray, redBright } from "console-log-colors";
import { getSection, readInput } from "./utils/file-utils";
import { CardinalDirection, parsePoint, Point } from "./utils/point";

const lines = readInput("day15", false);

function moveRobot(
  map: Map<string, string>,
  robot: Point,
  dir: CardinalDirection
): Point {
  // find all boxes, until we hit a wall or empty space
  const boxes = new Array<Point>();
  const robotStep = robot.step(dir);
  let p = robotStep;
  while (map.get(p.toString()) === "O") {
    boxes.push(p);
    p = p.step(dir);
  }

  // If we're not up against a wall, move the robot and any boxes.
  if (map.get(p.toString()) !== "#") {
    if (boxes.length !== 0) {
      // Just swap the first to the new "end", and put the robot
      // in its place.
      map.set(p.toString(), "O");
    }
    map.delete(robot.toString());
    map.set(robotStep.toString(), "@");
    robot = robotStep;
  }
  return robot;
}

function part1() {
  const map = sparseGrid(getSection(0, lines));
  const moves = getSection(1, lines)
    .map((e) => e.trim())
    .join();

  console.log("*** Map");
  printSparseGrid(map);
  console.log("\n\nMoves: ");
  console.log(moves);

  let robot: Point;
  map.forEach((v, k) => {
    if (v === "@") {
      robot = parsePoint(k);
    }
  });
  if (!robot) {
    console.log("Robot not found!");
    return;
  }
  console.log(`Robot starting at ${robot}`);

  for (let i = 0; i < moves.length; i++) {
    const move = moves[i];
    // console.log(`\n*** Moving ${move}`);

    if (move === "<") {
      robot = moveRobot(map, robot, CardinalDirection.W);
    } else if (move === ">") {
      robot = moveRobot(map, robot, CardinalDirection.E);
    } else if (move === "^") {
      robot = moveRobot(map, robot, CardinalDirection.N);
    } else if (move === "v") {
      robot = moveRobot(map, robot, CardinalDirection.S);
    }

    // printSparseGrid(map);
  }

  let sum = 0;
  map.forEach((v, k) => {
    if (v === "O") {
      const p = parsePoint(k);
      sum += 100 * p.y + p.x;
    }
  });

  console.log(`gps sum ${sum}`);
}

function isBox(p: Point, map: Grid<string>): boolean {
  return map.getValue(p) === "[" || map.getValue(p) === "]";
}

function isWideBox(v: string): boolean {
  return v === "[" || v === "]";
}

function canMoveBox(
  p: Point,
  dir: CardinalDirection,
  map: Grid<string>
): boolean {
  const other =
    map.getValue(p) === "["
      ? p.step(CardinalDirection.E)
      : p.step(CardinalDirection.W);

  const step = p.step(dir);
  const otherStep = other.step(dir);

  if (map.getValue(step) === "#" || map.getValue(otherStep) === "#")
    return false;

  if (isWideBox(map.getValue(step)!)) {
    if (!canMoveBox(step, dir, map)) return false;
  }
  if (isWideBox(map.getValue(otherStep)!)) {
    if (!canMoveBox(otherStep, dir, map)) return false;
  }

  return true;
}

function moveBox(p: Point, dir: CardinalDirection, map: Grid<string>) {
  const other =
    map.getValue(p) === "["
      ? p.step(CardinalDirection.E)
      : p.step(CardinalDirection.W);

  const step = p.step(dir);
  const otherStep = other.step(dir);

  if (isWideBox(map.getValue(step)!)) {
    moveBox(step, dir, map);
  }
  if (isWideBox(map.getValue(otherStep)!)) {
    moveBox(otherStep, dir, map);
  }

  map.setValue(step, map.getValue(p)!);
  map.setValue(otherStep, map.getValue(other)!);
  map.setValue(p, ".");
  map.setValue(other, ".");
}

function moveRobotWide(
  map: Grid<string>,
  robot: Point,
  dir: CardinalDirection
): Point {
  if (dir === CardinalDirection.W || dir === CardinalDirection.E) {
    // find all boxes, until we hit a wall or empty space
    const boxes = new Array<Point>();
    const robotStep = robot.step(dir);
    let p = robotStep;
    while (isBox(p, map)) {
      boxes.push(p);
      p = p.step(dir);
    }

    // If we're not up against a wall, move the robot and any boxes.
    if (map.getValue(p) !== "#") {
      for (let b = boxes.length - 1; b >= 0; b--) {
        const c = map.getValue(boxes[b]);
        map.setValue(boxes[b], ".");
        map.setValue(boxes[b].step(dir), c!);
      }
      map.setValue(robot, ".");
      map.setValue(robotStep, "@");
      robot = robotStep;
    }
  } else {
    const robotStep = robot.step(dir);

    const v = map.getValue(robotStep);
    if (v === ".") {
      map.setValue(robotStep, "@");
      map.setValue(robot, ".");
      robot = robotStep;
    } else if (v === "[" || v === "]") {
      if (canMoveBox(robotStep, dir, map)) {
        // move box and robot
        moveBox(robotStep, dir, map);
        map.setValue(robotStep, "@");
        map.setValue(robot, ".");
        robot = robotStep;
      }
    }
  }

  return robot;
}

function part2() {
  const styles = new Map([
    ["[", greenBG],
    ["]", greenBG],
    ["@", redBright],
    [".", gray],
  ]);
  const wideMapLines = getSection(0, lines).map((e) => {
    let wide = "";
    for (let i = 0; i < e.length; i++) {
      if (e[i] === "#") {
        wide += "##";
      } else if (e[i] === "O") {
        wide += "[]";
      } else if (e[i] === ".") {
        wide += "..";
      } else if (e[i] === "@") {
        wide += "@.";
      }
    }
    return wide;
  });
  const map = linesToCharGrid(wideMapLines);

  const moves = getSection(1, lines)
    .map((e) => e.trim())
    .join();

  // console.log("*** Map");
  // map.log(styles);
  // console.log("\n\nMoves:  ");
  // console.log(moves.length);
  // console.log(moves);

  let robot = map.find("@")!;
  console.log(`Robot starting at ${robot}`);

  for (let i = 0; i < moves.length; i++) {
    const move = moves[i];
    // console.log(`\n*** Moving ${move}`);

    if (move === "<") {
      robot = moveRobotWide(map, robot, CardinalDirection.W);
    } else if (move === ">") {
      robot = moveRobotWide(map, robot, CardinalDirection.E);
    } else if (move === "^") {
      robot = moveRobotWide(map, robot, CardinalDirection.N);
    } else if (move === "v") {
      robot = moveRobotWide(map, robot, CardinalDirection.S);
    }

    // map.log();
  }

  // printSparseGrid(map);

  let sum = BigInt(0);
  map.iterate((x, y, s) => {
    if (s === "[") {
      sum += BigInt(100 * y) + BigInt(x);
    }
  });

  console.log(`gps sum ${sum}`);
}

console.time();
part2();
console.timeEnd();
