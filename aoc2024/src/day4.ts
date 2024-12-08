import {readInput} from './utils/file-utils';
import {Point, CardinalDirection} from './utils/point';
import {gridValue, findSequence} from './utils/char-grid';

let lines = readInput('day4', false);


function part1() {
    const results = findSequence('XMAS', lines);
    let count = 0;
    results.forEach(result => {
        count += result.dirs.length;
    });
    console.log(`found xmas ${count} times`)
}

function part2() {
    let count = 0;
    for (let y = 0; y < lines.length; y++) {
        const line = lines[y];
        for (let x = 0; x < line.length; x++) {
            const start = new Point(x, y);
            if (lines[start.y][start.x] === 'A') {
                const nw = start.step(CardinalDirection.NW);
                const se = start.step(CardinalDirection.SE);
                const nwValue = gridValue(nw, lines);
                const seValue = gridValue(se, lines);
                const fromWest = (nwValue === 'M' && seValue === 'S') || (nwValue === 'S' && seValue == 'M');

                const ne = start.step(CardinalDirection.NE);
                const sw = start.step(CardinalDirection.SW);
                const neValue = gridValue(ne, lines);
                const swValue = gridValue(sw, lines);
                const fromEast = (neValue === 'M' && swValue === 'S') || (neValue === 'S' && swValue == 'M');

                if (fromWest && fromEast) {
                    count++;
                }
            }
        }        
    }
    console.log(`Found ${count} x-mas`)
}

part2();
