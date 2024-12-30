import { Grid, linesToGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day10", false);

function countPathsToNineFromStep(
  grid: Grid<number>,
  from: Point,
  dir: CardinalDirection,
  path: Point[],
  completePaths: Point[][]
) {
  const fromValue = grid.getValue(from)!;
  const nextNorth = from.step(dir);
  if (nextNorth && path.findIndex((e) => e.equals(nextNorth)) === -1) {
    const nextNorthValue = grid.getValue(nextNorth);
    // visited.push(nextNorth);
    if (nextNorthValue === fromValue + 1) {
      if (nextNorthValue === 9) {
        // console.log(`reached 9 from path ${path.join(" ")}`);
        completePaths.push(path.concat([nextNorth]));
      } else {
        // console.log(
        //   `following path from ${from} (${fromValue}) ${dir} to ${nextNorth} (${nextNorthValue}): ${path.join(" ")}`
        // );
        countPathsToNine(grid, nextNorth, path, completePaths);
      }
    }
  }
}

function countPathsToNine(
  grid: Grid<number>,
  from: Point,
  path: Point[],
  completePaths: Point[][]
): number {
  const nextPath = path.concat([from]);
  countPathsToNineFromStep(
    grid,
    from,
    CardinalDirection.N,
    nextPath,
    completePaths
  );
  countPathsToNineFromStep(
    grid,
    from,
    CardinalDirection.S,
    nextPath,
    completePaths
  );
  countPathsToNineFromStep(
    grid,
    from,
    CardinalDirection.E,
    nextPath,
    completePaths
  );
  countPathsToNineFromStep(
    grid,
    from,
    CardinalDirection.W,
    nextPath,
    completePaths
  );

  return completePaths.length;
}

function part1() {
  const grid = linesToGrid(lines, parseInt);
  console.log(grid);
  let total = 0;
  grid.iterate((x, y, c) => {
    if (c === 0) {
      console.log(`starting at ${x}, ${y}`);
      const paths = new Array<Point[]>();
      const count = countPathsToNine(grid, new Point(x, y), [], paths);
      //   console.log(`found ${count} from ${x}, ${y}`);
      const uniqueNines = new Set<string>();
      for (let i = 0; i < paths.length; i++) {
        const p = paths[i][paths[i].length - 1];
        uniqueNines.add(p.toString());
      }
      console.log(`**** found ${uniqueNines.size} from ${x},${y}`);
      total += uniqueNines.size;
    }
  });
  console.log(`total ${total}`);
}

function part2() {
  const grid = linesToGrid(lines, parseInt);
  // console.log(grid);
  let total = 0;
  grid.iterate((x, y, c) => {
    if (c === 0) {
      console.log(`starting at ${x}, ${y}`);
      const paths = new Array<Point[]>();
      const count = countPathsToNine(grid, new Point(x, y), [], paths);
      //   console.log(`found ${count} from ${x}, ${y}`);
      // console.log(`**** found ${paths.length} from ${x},${y}`);
      total += paths.length;
    }
  });
  console.log(`total ${total}`);
}

console.time();
part2();
console.timeEnd();
