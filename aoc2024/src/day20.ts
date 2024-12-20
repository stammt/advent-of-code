import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, parsePoint, Point } from "./utils/point";

const lines = readInput("day20", false);

type Cheat = {
  cheatSteps: Point[];
  stepsSaved: number;
};

function getNonWallNeighbors(p: Point, track: Grid<string>): Point[] {
  const neighbors = [
    p.step(CardinalDirection.N),
    p.step(CardinalDirection.S),
    p.step(CardinalDirection.E),
    p.step(CardinalDirection.W),
  ];
  return neighbors.filter((e) => track.getValue(e) !== "#");
}

function getStepsSaved(
  p: Point,
  wall: Point,
  steps: Map<string, number>,
  track: Grid<string>
): Cheat {
  // Find the non-wall neighbors of this wall, excluding the current step
  const nextSteps = getNonWallNeighbors(wall, track).filter(
    (e) => !e.equals(p)
  );
  // steps up to p
  const currentStepCount = steps.get(p.toString())!;
  const cheatingStepCount = currentStepCount + 2;
  let bestStepsSaved = 0;
  let cheatingSteps: Point[] = [];
  nextSteps.forEach((s) => {
    // steps up to s without cheating
    const baseStepCount = steps.get(s.toString())!;
    if (cheatingStepCount < baseStepCount) {
      const saved = baseStepCount - cheatingStepCount;
      if (saved > bestStepsSaved) {
        bestStepsSaved = saved;
        cheatingSteps = [wall, s];
      }
    }
  });
  return { cheatSteps: cheatingSteps, stepsSaved: bestStepsSaved };
}

function part1() {
  const track = linesToCharGrid(lines);
  const start = track.find("S");

  // there aren't any branchs, so just follow the path and
  // track how many steps are taken at each position. Then
  // try taking out each piece of wall and compare the new
  // number of steps.
  let p = start;
  const steps = new Map<string, number>();
  steps.set(start.toString(), 0);
  let stepCount = 0;
  while (true) {
    // find the next step
    const nextSteps = getNonWallNeighbors(p, track).filter(
      (e) => !steps.has(e.toString())
    );
    if (nextSteps.length > 1) {
      console.log(`***** found a branch at ${p}`);
      break;
    } else {
      p = nextSteps[0];
      steps.set(p.toString(), ++stepCount);
    }

    if (track.getValue(p) === "E") {
      console.log(
        `found the end after ${steps.get(p.toString())} steps at ${p}`
      );
      break;
    }
  }

  const cheats = new Map<number, Cheat[]>();

  steps.forEach((stepCount, step) => {
    // For each wall adjacent to this step, find the step on the path next
    // to that wall with the highest step value. If that step value is less
    // than this step's value + 1 then we've saved a step.
    const p = parsePoint(step);
    [
      CardinalDirection.N,
      CardinalDirection.S,
      CardinalDirection.E,
      CardinalDirection.W,
    ].forEach((dir) => {
      const s = p.step(dir);
      if (track.getValue(s) === "#") {
        const cheat = getStepsSaved(p, s, steps, track);
        if (cheat.stepsSaved > 0) {
          if (cheats.has(cheat.stepsSaved)) {
            cheats.get(cheat.stepsSaved)?.push(cheat);
          } else {
            cheats.set(cheat.stepsSaved, [cheat]);
          }
        }
      }
    });
  });

  let over100 = 0;
  cheats.forEach((cheats, stepsSaved) => {
    console.log(`${cheats.length} save ${stepsSaved}`);
    if (stepsSaved >= 100) {
      over100 += cheats.length;
    }
  });

  // 393 too low
  console.log(`${over100} save at least 100`);
}

function part2() {}

part1();
