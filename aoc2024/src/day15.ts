import {
  Grid,
  linesToCharGrid,
  linesToGrid,
  printSparseGrid,
  sparseGrid,
  toNumberGrid,
} from "./utils/char-grid";
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

function isBox(p: Point, map: Map<string, string>): boolean {
  return map.get(p.toString()) === "[" || map.get(p.toString()) === "]";
}

function getBoxesInRange(
  y: number,
  startx: number,
  endx: number,
  map: Map<string, string>
): Point[][] {
  const boxes = new Set<string>();
  const results = new Array<Point[]>();
  for (let x = startx; x <= endx; x++) {
    const p = new Point(x, y);
    if (!boxes.has(p.toString())) {
      if (map.get(p.toString()) === "[") {
        boxes.add(p.toString());
        results.push([p, p.step(CardinalDirection.E)]);
      } else if (map.get(p.toString()) === "]") {
        const boxStart = p.step(CardinalDirection.W);
        boxes.add(boxStart.toString());
        results.push([boxStart, p]);
      }
    }
  }
  return results;
}

function isWallInRange(
  y: number,
  startx: number,
  endx: number,
  map: Map<string, string>
): boolean {
  for (let x = startx; x <= endx; x++) {
    if (map.get(new Point(x, y).toString()) === "#") {
      return true;
    }
  }
  return false;
}

function moveRobotWide(
  map: Map<string, string>,
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
    if (map.get(p.toString()) !== "#") {
      for (let b = boxes.length - 1; b >= 0; b--) {
        const c = map.get(boxes[b].toString());
        map.delete(boxes[b].toString());
        map.set(boxes[b].step(dir).toString(), c!);
      }
      map.delete(robot.toString());
      map.set(robotStep.toString(), "@");
      robot = robotStep;
    }
  } else {
    // find all boxes, until we hit a wall or empty space. Each box is two points.
    const boxes = new Array<Point[]>();
    const robotStep = robot.step(dir);
    let p = robotStep;
    // the start and end of the row of boxes being pushed, if any
    let pushStart = p.x;
    let pushEnd = p.x;
    while (true) {
      console.log(`checking push row ${p.y} from ${pushStart} to ${pushEnd}`);
      if (isWallInRange(p.y, pushStart, pushEnd, map)) {
        console.log(`hit the wall`);
        break;
      }
      const boxesInRange = getBoxesInRange(p.y, pushStart, pushEnd, map);
      if (boxesInRange.length > 0) {
        boxes.push(...boxesInRange);
        pushStart = boxesInRange[0][0].x;
        pushEnd = boxesInRange[boxesInRange.length - 1][1].x;
        console.log(`Will push boxes ${boxesInRange}`);
        p = p.step(dir);
      } else {
        break;
      }
    }

    // If we're not up against a wall, move the robot and any boxes.
    if (!isWallInRange(p.y, pushStart, pushEnd, map)) {
      for (let b = boxes.length - 1; b >= 0; b--) {
        map.set(boxes[b][0].step(dir).toString(), "[");
        map.set(boxes[b][1].step(dir).toString(), "]");
        map.delete(boxes[b][0].toString());
        map.delete(boxes[b][1].toString());
      }
      map.delete(robot.toString());
      map.set(robotStep.toString(), "@");
      robot = robotStep;
    }
  }

  return robot;
}

function part2() {
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
  const map = sparseGrid(wideMapLines);
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
    console.log(`\n*** Moving ${move}`);

    if (move === "<") {
      robot = moveRobotWide(map, robot, CardinalDirection.W);
    } else if (move === ">") {
      robot = moveRobotWide(map, robot, CardinalDirection.E);
    } else if (move === "^") {
      robot = moveRobotWide(map, robot, CardinalDirection.N);
    } else if (move === "v") {
      robot = moveRobotWide(map, robot, CardinalDirection.S);
    }

    printSparseGrid(map);
  }

  // printSparseGrid(map);

  let sum = 0;
  map.forEach((v, k) => {
    if (v === "[") {
      const p = parsePoint(k);
      sum += 100 * p.y + p.x;
    }
  });

  // 1540869 too low

  console.log(`gps sum ${sum}`);
}

part2();
