import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, parsePoint, Point } from "./utils/point";

const lines = readInput("day20", false);

type Cheat = {
  cheatSteps: Point[];
  stepsSaved: number;
};

function getSteps(start: Point, track: Grid<string>): Map<string, number> {
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
  return steps;
}

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

  const steps = getSteps(start, track);
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

  console.log(`${over100} save at least 100`);
}

function cheatString(cheat: Cheat) {
  return `${cheat.cheatSteps[0]}-${cheat.cheatSteps[1]}`;
}

function dist(p1: Point, p2: Point): number {
  return Math.abs(p1.x - p2.x) + Math.abs(p1.y - p2.y);
}

function findCheatsFromPoint(
  cheatStart: Point,
  steps: Map<string, number>,
  track: Grid<string>
): Cheat[] {
  const MAX_CHEAT_LENGTH = 20;
  const results: Cheat[] = [];

  // Find all the points within 20 steps of this one.
  // For each point that is on the track, add the cheat if it would save time.
  const startStepCount = steps.get(cheatStart.toString())!;

  // could optimize by limiting x and y to within 20 of the current point
  for (let y = 0; y < track.grid.length; y++) {
    for (let x = 0; x < track.grid[y].length; x++) {
      const p = new Point(x, y);
      const distance = dist(cheatStart, p);
      if (distance <= MAX_CHEAT_LENGTH) {
        const baseStepCount = steps.get(p.toString())!;
        const cheatingStepCount = startStepCount + distance;
        if (cheatingStepCount < baseStepCount) {
          // console.log(`Found cheat from ${cheatStart} to ${s}`);
          results.push({
            cheatSteps: [cheatStart, p],
            stepsSaved: baseStepCount - cheatingStepCount,
          });
        }
      }
    }
  }

  return results;
}

function part2() {
  const track = linesToCharGrid(lines);
  const start = track.find("S");

  const steps = getSteps(start, track);

  // map of steps saved -> number of cheats that save this amount of steps
  const cheats = new Map<number, number>();

  steps.forEach((stepCount, step) => {
    // get the raw list of cheats from this point
    const rawCheatsFromPoint = findCheatsFromPoint(
      parsePoint(step),
      steps,
      track
    );

    // de-dupe them and pick the lowest step count for each
    const cheatsFromPoint = new Map<string, number>();
    rawCheatsFromPoint.forEach((rawCheat) => {
      const s = cheatString(rawCheat);
      if (cheatsFromPoint.has(s)) {
        const other = cheatsFromPoint.get(s)!;
        // Don't think this should happen?
        if (rawCheat.stepsSaved < other) {
          cheatsFromPoint.set(s, rawCheat.stepsSaved);
        }
      } else {
        cheatsFromPoint.set(s, rawCheat.stepsSaved);
      }
    });

    // then add these to the main map of cheats
    cheatsFromPoint.forEach((stepsSaved, cheatString) => {
      if (cheats.has(stepsSaved)) {
        cheats.set(stepsSaved, cheats.get(stepsSaved)! + 1);
      } else {
        cheats.set(stepsSaved, 1);
      }
    });
  });

  let over100 = 0;
  cheats.forEach((cheats, stepsSaved) => {
    if (stepsSaved >= 100) {
      console.log(`${cheats} save ${stepsSaved}`);
      over100 += cheats;
    }
  });

  console.log(`${over100} save at least 100`);
}

part2();
