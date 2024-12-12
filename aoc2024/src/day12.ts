import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day12", false);

function expandPlot(
  dir: CardinalDirection,
  plant: string,
  start: Point,
  currentPlots: Point[],
  plot: Grid<string>
) {
  const n = start.step(dir);
  if (
    plot.isValid(n) &&
    plot.getValue(n) === plant &&
    !currentPlots.find((e) => e.equals(n))
  ) {
    currentPlots.push(n);
    buildPlot(plant, n, currentPlots, plot);
  }
}

function buildPlot(
  plant: string,
  start: Point,
  currentPlots: Point[],
  plot: Grid<string>
) {
  expandPlot(CardinalDirection.N, plant, start, currentPlots, plot);
  expandPlot(CardinalDirection.S, plant, start, currentPlots, plot);
  expandPlot(CardinalDirection.E, plant, start, currentPlots, plot);
  expandPlot(CardinalDirection.W, plant, start, currentPlots, plot);
}

function calculatePerimeter(plot: Point[]): number {
  let perimeter = 0;
  for (let i = 0; i < plot.length; i++) {
    let p = 4;
    if (plot.find((e) => e.equals(plot[i].step(CardinalDirection.N)))) p--;
    if (plot.find((e) => e.equals(plot[i].step(CardinalDirection.S)))) p--;
    if (plot.find((e) => e.equals(plot[i].step(CardinalDirection.E)))) p--;
    if (plot.find((e) => e.equals(plot[i].step(CardinalDirection.W)))) p--;
    perimeter += p;
  }
  return perimeter;
}

function buildPlots(garden: Grid<string>): Point[][] {
  const visited = new Set<string>();
  const plots = new Array<Point[]>();

  for (let y = 0; y < garden.grid.length; y++) {
    for (let x = 0; x < garden.grid[y].length; x++) {
      const p = new Point(x, y);
      if (!visited.has(p.toString())) {
        const plant = garden.getValue(p)!;
        const currentPlots = new Array<Point>();
        currentPlots.push(p);
        buildPlot(plant, p, currentPlots, garden);
        currentPlots.forEach((point) => {
          visited.add(point.toString());
        });
        plots.push(currentPlots);
        console.log(`Plant ${plant} : ${currentPlots.join(" ")}`);
      }
    }
  }
  return plots;
}

function part1() {
  const garden = linesToCharGrid(lines);

  const plots = buildPlots(garden);

  let sum = 0;
  for (let i = 0; i < plots.length; i++) {
    const perimeter = calculatePerimeter(plots[i]);
    const price = perimeter * plots[i].length;
    sum += price;
    console.log(
      `perimeter is ${perimeter}, price is ${price} for ${plots[i].join(" ")}`
    );
  }
  console.log(`total price ${sum}`);
}

function countSides(plot: Point[], garden: Grid<string>): number {
  let count = 0;

  // look for top and bottom sides
  for (let y = 0; y < garden.grid.length; y++) {
    // get all plots on this row in order
    const row = plot.filter((e) => e.y === y).sort((a, b) => a.x - b.x);

    let lastTopEdge;
    let lastBottomEdge;
    for (let x = 0; x < row.length; x++) {
      const p = row[x];
      const above = p.step(CardinalDirection.N);
      const below = p.step(CardinalDirection.S);

      const isTopEdge = garden.getValue(above) !== garden.getValue(p);
      const isBottomEdge = garden.getValue(below) !== garden.getValue(p);

      if (isTopEdge) {
        if (lastTopEdge != p.x - 1) {
          // console.log(`${garden.getValue(p)} Starting new top edge with ${p}`);
          count += 1;
        }
        lastTopEdge = p.x;
      }
      if (isBottomEdge) {
        if (lastBottomEdge != p.x - 1) {
          // console.log(`${garden.getValue(p)} Starting new bottom edge with ${p}`);
          count += 1;
        }
        lastBottomEdge = p.x;
      }
    }
  }

  // look for left and right sides
  for (let x = 0; x < garden.grid[0].length; x++) {
    // get all plots on this column in order
    const col = plot.filter((e) => e.x === x).sort((a, b) => a.y - b.y);

    let lastLeftEdge;
    let lastRightEdge;
    for (let y = 0; y < col.length; y++) {
      const p = col[y];
      const left = p.step(CardinalDirection.W);
      const right = p.step(CardinalDirection.E);

      const isLeftEdge = garden.getValue(left) !== garden.getValue(p);
      const isRightEdge = garden.getValue(right) !== garden.getValue(p);

      if (isLeftEdge) {
        if (lastLeftEdge !== p.y - 1) {
          //   console.log(`${garden.getValue(p)} Starting new left edge with ${p}`);
          count += 1;
          // } else {
          //   console.log(`${garden.getValue(p)} Continuing left edge with ${p}`);
        }

        lastLeftEdge = p.y;
      }
      if (isRightEdge) {
        if (lastRightEdge !== p.y - 1) {
          //   console.log(
          //     `${garden.getValue(p)} Starting new right edge with ${p}`
          //   );
          count += 1;
          // } else {
          //   console.log(`${garden.getValue(p)} Continuing right edge with ${p}`);
        }
        lastRightEdge = p.y;
      }
    }
  }

  return count;
}

function part2() {
  const garden = linesToCharGrid(lines);

  const plots = buildPlots(garden);

  let sum = 0;
  for (let i = 0; i < plots.length; i++) {
    const sides = countSides(plots[i], garden);
    const price = sides * plots[i].length;
    sum += price;
    console.log(
      `${garden.getValue(plots[i][0])} sides is ${sides}, price is ${price} for ${plots[i].join(" ")}`
    );
  }
  console.log(`total price ${sum}`);
}

part2();
