export enum CardinalDirection {
  N = "N",
  NE = "NE",
  E = "E",
  SE = "SE",
  S = "S",
  SW = "SW",
  W = "W",
  NW = "NW",
}
export const CardinalDirections = [
  CardinalDirection.N,
  CardinalDirection.NE,
  CardinalDirection.E,
  CardinalDirection.SE,
  CardinalDirection.S,
  CardinalDirection.SW,
  CardinalDirection.W,
  CardinalDirection.NW,
];

export class Point {
  readonly x: number;
  readonly y: number;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }

  step(direction: CardinalDirection): Point {
    let nextX = this.x;
    let nextY = this.y;
    if (
      direction == CardinalDirection.N ||
      direction == CardinalDirection.NE ||
      direction == CardinalDirection.NW
    ) {
      nextY -= 1;
    } else if (
      direction == CardinalDirection.S ||
      direction == CardinalDirection.SE ||
      direction == CardinalDirection.SW
    ) {
      nextY += 1;
    }
    if (
      direction == CardinalDirection.W ||
      direction == CardinalDirection.NW ||
      direction == CardinalDirection.SW
    ) {
      nextX -= 1;
    } else if (
      direction == CardinalDirection.E ||
      direction == CardinalDirection.NE ||
      direction == CardinalDirection.SE
    ) {
      nextX += 1;
    }
    return new Point(nextX, nextY);
  }

  stepBy(step: Point, wrap: boolean = false, gridSize?: Point): Point {
    if (wrap) {
      const x = wrapPoint(this.x + step.x, gridSize!.x);
      const y = wrapPoint(this.y + step.y, gridSize!.y);
      return new Point(x, y);
    } else {
      return new Point(this.x + step.x, this.y + step.y);
    }
  }

  toString(): string {
    return `${this.x},${this.y}`;
  }

  equals(other?: Point): boolean {
    return other != undefined && this.x === other.x && this.y === other.y;
  }
}

export function wrapPoint(x: number, max: number): number {
  if (x >= 0 && x < max) return x;

  if (x < 0) {
    return max + x;
  } else {
    return x % max;
  }
}

export function parsePoint(s: string): Point {
  const [x, y] = s.split(",").map((e) => parseInt(e));
  return new Point(x, y);
}
