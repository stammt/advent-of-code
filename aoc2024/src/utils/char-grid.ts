import { Point, CardinalDirection, CardinalDirections } from "./point.ts";

export class Grid<T> {
  readonly grid: T[][];

  constructor(grid: T[][]) {
    this.grid = grid;
  }

  iterate(cb: (x: number, y: number, s: T) => void): void {
    for (let y = 0; y < this.grid.length; y++) {
      for (let x = 0; x < this.grid[y].length; x++) {
        cb(x, y, this.grid[y][x]);
      }
    }
  }

  isValid(point: Point): boolean {
    return (
      point.y >= 0 &&
      point.y < this.grid.length &&
      point.x >= 0 &&
      point.x < this.grid[point.y].length
    );
  }

  getValue(point: Point): T | undefined {
    if (!this.isValid(point)) return undefined;

    return this.grid[point.y][point.x];
  }
}

export function iterateGrid(
  grid: string[],
  cb: (x: number, y: number, s: string) => void
): void {
  for (let y = 0; y < grid.length; y++) {
    for (let x = 0; x < grid[y].length; x++) {
      cb(x, y, grid[y][x]);
    }
  }
}

export function linesToGrid<T>(
  lines: string[],
  mapper: (value: string) => T
): Grid<T> {
  const result = new Array<T[]>(lines.length);

  for (let y = 0; y < lines.length; y++) {
    const line = new Array<T>(lines[y].length);
    for (let x = 0; x < lines[y].length; x++) {
      line[x] = mapper(lines[y][x]);
    }
    result[y] = line;
  }
  return new Grid(result);
}

export function linesToNumberGrid(lines: string[]): Grid<number> {
  return linesToGrid(lines, parseInt);
}

export function linesToCharGrid(lines: string[]): Grid<string> {
  return linesToGrid(lines, (e) => e);
}

// returns the char at the given point, or undefined if it is not in the grid
export function gridValue(point: Point, grid: string[]): string | undefined {
  if (!isOnTheGrid(point, grid)) return undefined;

  return grid[point.y][point.x];
}

// returns true if the point is in the grid, false otherwise
export function isOnTheGrid(point: Point, grid: string[]): boolean {
  return (
    point.y >= 0 &&
    point.y < grid.length &&
    point.x >= 0 &&
    point.x < grid[point.y].length
  );
}

// finds the given sequence in the grid, returning all start positions and directions that are found
export function findSequence(
  seq: string,
  grid: string[]
): { start: Point; dirs: Array<CardinalDirection> }[] {
  const results: { start: Point; dirs: Array<CardinalDirection> }[] = [];

  for (let y = 0; y < grid.length; y++) {
    const line = grid[y];
    for (let x = 0; x < line.length; x++) {
      const start = new Point(x, y);
      const dirs = followSequence(seq, start, grid);
      if (dirs.length > 0) {
        results.push({ start: start, dirs: dirs });
      }
    }
  }
  return results;
}

function followSequence(
  seq: string,
  point: Point,
  grid: string[]
): CardinalDirection[] {
  const results = new Array<CardinalDirection>();
  for (let i = 0; i < CardinalDirections.length; i++) {
    let nextPoint = point;
    const dir = CardinalDirections[i];
    for (let seqIndex = 0; seqIndex < seq.length; seqIndex++) {
      if (!isOnTheGrid(nextPoint, grid)) break;
      if (grid[nextPoint.y][nextPoint.x] !== seq[seqIndex]) break;

      if (seqIndex === seq.length - 1) {
        results.push(dir);
      } else {
        nextPoint = nextPoint.step(dir);
      }
    }
  }
  return results;
}
