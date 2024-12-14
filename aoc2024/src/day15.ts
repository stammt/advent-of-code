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
      s += c.length === 0 ? "." : c.length;
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

function part2() {}

part1();
