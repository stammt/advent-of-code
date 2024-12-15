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

const lines = readInput("day15", true);

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

function part2() {}

part1();
