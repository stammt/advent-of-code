import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, parsePoint, Point } from "./utils/point";

const lines = readInput("day15", false);

type Robot = {
  pos: Point;
  step: Point;
};

function parseRobot(line: string): Robot {
  const [p, s] = line.split(" ");
  const pos = parsePoint(p.split("=")[1]);
  const step = parsePoint(s.split("=")[1]);
  return { pos: pos, step: step };
}

function printGrid(robots: Robot[], gridSize: Point) {
  for (let y = 0; y < gridSize.y; y++) {
    let s = "";
    for (let x = 0; x < gridSize.x; x++) {
      const c = robots.filter((e) => e.pos.x === x && e.pos.y === y);
      s += c.length === 0 ? "." : "X";
    }
    console.log(s);
  }
  console.log("");
}

function part1() {
  const gridSize = new Point(101, 103);
  const secs = 100;
  const robots = lines.map((e) => parseRobot(e));

  printGrid(robots, gridSize);
  robots.forEach((robot) => {
    for (let i = 0; i < secs; i++) {
      robot.pos = robot.pos.stepBy(robot.step, true, gridSize);
    }
  });
  //   printGrid(robots, gridSize);

  const midX = Math.floor(gridSize.x / 2);
  const midY = Math.floor(gridSize.y / 2);
  console.log(`midX ${midX}, midY ${midY}`);

  const q1 = robots.filter((r) => r.pos.x < midX && r.pos.y < midY);
  const q2 = robots.filter((r) => r.pos.x < midX && r.pos.y > midY);
  const q3 = robots.filter((r) => r.pos.x > midX && r.pos.y < midY);
  const q4 = robots.filter((r) => r.pos.x > midX && r.pos.y > midY);
  const total = q1.length * q2.length * q3.length * q4.length;

  console.log(
    `safety factor ${total} ${q1.length} ${q2.length} ${q3.length} ${q4.length}`
  );
}

function isTreeShaped(robots: Robot[], gridSize: Point): boolean {
  // sort into the grid order to look for a christmas tree...?
  robots.sort((a, b) => {
    if (a.pos.y !== b.pos.y) {
      return a.pos.y - b.pos.y;
    }
    return a.pos.x - b.pos.x;
  });

  const row = robots[0].pos.y;
  let lastRowStart = Infinity;
  let lastRowEnd = -Infinity;
  let maybe = true;
  for (let y = row; y < gridSize.y; y++) {
    const robotsInRow = robots.filter((r) => r.pos.y === y);
    //   console.log(`${robotsInRow.length} in row ${y}`);
    if (robotsInRow.length === 0) {
      const leftovers = robots.filter((r) => r.pos.y > y);
      if (leftovers.length > 0) {
        maybe = false;
      }
      break;
    }
    const rowStart = robotsInRow[0].pos.x;
    const rowEnd = robotsInRow[robotsInRow.length - 1].pos.x;
    //   console.log(`Row ${y} has width ${rowWidth}`);
    if (rowStart > lastRowStart || rowEnd < lastRowEnd) {
      maybe = false;
      break;
    }
    lastRowStart = rowStart;
    lastRowEnd = rowEnd;
  }

  return maybe;
}

function isTreeShapedRows(
  rows: Map<number, number[]>,
  firstRow: number,
  lastRow: number,
  gridSize: Point
): boolean {
  let lastRowStart = Infinity;
  let lastRowEnd = -Infinity;
  let maybe = true;
  for (let y = firstRow; y < gridSize.y; y++) {
    const exes = rows.get(y);
    if (!exes) {
      // empty row
      if (y < lastRow) {
        // console.log("leftover rows");
        maybe = false;
      }
      break;
    }
    exes!.sort((a, b) => a - b);
    // console.log(`row ${y} exes ${exes}`);
    if (exes[0] > lastRowStart) {
      //   console.log(`row ${y} starts ${exes[0]} after ${lastRowStart}`);
      maybe = false;
      break;
    }
    if (exes[exes.length - 1] < lastRowEnd) {
      //   console.log(`row ${y} ends ${exes[exes.length - 1]} after ${lastRowEnd}`);
      maybe = false;
      break;
    }
    lastRowStart = exes[0];
    lastRowEnd = exes[exes.length - 1];
  }

  return maybe;
}

async function part2() {
  const gridSize = new Point(101, 103);
  const secs = 10000;
  const robots = lines.map((e) => parseRobot(e));

  printGrid(robots, gridSize);
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  for (let i = 0; i < secs; i++) {
    const rows = new Map<number, number[]>();
    let firstRow = Infinity;
    let lastRow = -Infinity;

    robots.forEach((robot) => {
      robot.pos = robot.pos.stepBy(robot.step, true, gridSize);
      firstRow = Math.min(firstRow, robot.pos.y);
      lastRow = Math.max(lastRow, robot.pos.y);
      if (rows.has(robot.pos.y)) {
        rows.get(robot.pos.y)?.push(robot.pos.x);
      } else {
        rows.set(robot.pos.y, [robot.pos.x]);
      }
    });

    // console.log(1)
    // await sleep(150);
    if (i > 6500 && i < 7000) {
      printGrid(robots, gridSize);
      console.log(`iteration ${i}`);
    }
    // console.log(2)

    // if (isTreeShapedRows(rows, firstRow, lastRow, gridSize)) {
    //   printGrid(robots, gridSize);
    //   console.log(`Might be a tree after ${i}`);
    //   break;
    // }

    if (i % 10000 === 0) {
      console.log(`iteration ${i}`);
    }

    // if (isTreeShaped(robots, gridSize)) {
    //   printGrid(robots, gridSize);
    //   console.log(`Might be a tree after ${i}`);
    // }
  }
  //   printGrid(robots, gridSize);
}

function testTree() {
  const robotTree: Array<Robot> = [
    { pos: new Point(10, 0), step: new Point(0, 0) },
    { pos: new Point(9, 1), step: new Point(0, 0) },
    { pos: new Point(12, 1), step: new Point(0, 0) },
    { pos: new Point(7, 2), step: new Point(0, 0) },
    { pos: new Point(13, 2), step: new Point(0, 0) },
    { pos: new Point(5, 3), step: new Point(0, 0) },
    { pos: new Point(14, 3), step: new Point(0, 0) },
  ];
  printGrid(robotTree, new Point(20, 20));
  const isTree = isTreeShaped(robotTree, new Point(20, 20));
  console.log(`isTree? ${isTree}`);
}

function testTreeRows() {
  const robotTreeRows = new Map<number, number[]>();
  robotTreeRows.set(0, [10]);
  robotTreeRows.set(1, [9, 12]);
  robotTreeRows.set(2, [7, 13]);
  robotTreeRows.set(3, [14, 5]);
  //   printGrid(robotTree, new Point(20, 20));
  const isTree = isTreeShapedRows(robotTreeRows, 0, 3, new Point(20, 20));
  console.log(`isTree? ${isTree}`);
}

part2();
