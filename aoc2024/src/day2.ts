import {readInput} from './utils/file-utils';

let lines = readInput('day2', false);

function isSafe(line: String) : Boolean {
    const levels = line.split(' ').map(e => parseInt(e));
    const increasing = levels[0] < levels[1];

    for (let i = 1; i < levels.length; i++) {
        if (levels[i] == levels[i-1]) return false;
        if (Math.abs(levels[i] - levels[i-1]) > 3) return false;
        if ((levels[i] > levels[i-1]) != increasing) return false;
    }

    return true;
}

function part1() {
    var sum = 0;
    lines.forEach(line => {
        const safe = isSafe(line);
        // console.log(`safe: ${safe} for ${line}`)
        if (safe) sum+=1;
    });
    console.log(`safe count ${sum}`)
}

function isSafeDampened(line: String) : Boolean {
    if (isSafe(line)) return true;

    const levels = line.split(' ');

    for (let i = 0; i < levels.length; i++) {
        const dampened = Array.from(levels);
        dampened.splice(i, 1);
        const safe = isSafe(dampened.join(' '));
        if (safe) {
            console.log(`${levels} is safe after removing ${i} (${dampened.join(' ')})`)
        }
        if (safe) return true;
    }
    return false;
}

function part2() {
    var sum = 0;
    lines.forEach(line => {
        const safe = isSafeDampened(line);
        console.log(`safe: ${safe} for ${line}`)
        if (safe) sum+=1;
    });

    console.log(`safe count ${sum}`)
}

part2();
