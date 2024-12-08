import {Point, CardinalDirection, CardinalDirections} from './point.ts';

export function gridValue(point: Point, grid: String[]) : string | undefined {
    if (!isOnTheGrid(point, grid)) return undefined;

    return grid[point.y][point.x];
}

export function isOnTheGrid(point: Point, grid: String[]) : boolean {
    return point.y >= 0 && point.y < grid.length && point.x >= 0 && point.x < grid[point.y].length
}

export function findSequence(seq: String, grid: String[]) : { start: Point, dirs: Array<CardinalDirection> }[] {
    const results: { start: Point, dirs: Array<CardinalDirection> }[] = new Array();

    for (let y = 0; y < grid.length; y++) {
        const line = grid[y];
        for (let x = 0; x < line.length; x++) {
            const start = new Point(x, y);
            const dirs = followSequence(seq, start, grid);
            if (dirs.length > 0) {
                results.push({start: start, dirs: dirs})
            }
        }        
    };
    return results;
}

function followSequence(seq: String, point: Point, grid: String[]) : CardinalDirection[] {
    const results = new Array<CardinalDirection>();
    for (let i = 0; i < CardinalDirections.length; i++) {
        let nextPoint = point;
        const dir = CardinalDirections[i]
        for (let seqIndex = 0; seqIndex < seq.length; seqIndex++) {
            if (!isOnTheGrid(nextPoint, grid)) break;
            if (grid[nextPoint.y][nextPoint.x] !== seq[seqIndex]) break;

            if (seqIndex === seq.length - 1) {
                results.push(dir)
            } else {
                nextPoint = nextPoint.step(dir);
            }
        }
    }
    return results;
}
