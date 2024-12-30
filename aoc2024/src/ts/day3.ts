import {readInput} from './utils/file-utils';

let lines = readInput('day3', false);


function part1() {
    const mulRegex = /mul\((\d+),(\d+)\)/gd

    var sum = BigInt(0)
    lines.forEach(line => {        
        const matches = line.matchAll(mulRegex);

        if (matches) {
            for (let match of matches) {
                const index = match.indices
                const product = parseInt(match[1]) * parseInt(match[2]);

                // console.log(`match: ${match[0]} - ${match[1]} ${match[2]} = ${product}`)
                sum = sum + BigInt(product)
            };
        } else {
            console.log('No mul found')
        }
    });
    console.log(`sum: ${sum}`)
}

function part2() {
    const mulRegex = /mul\((\d+),(\d+)\)/gd
    const doRegex = /do\(\)/gd
    const dontRegex = /don\'t\(\)/gd


    var sum = BigInt(0)
    var enabled = true;

    lines.forEach(line => {        
        const matches = line.matchAll(mulRegex);
        var matchIndex = 0;

        var index = 0;
        if (matches) {
            for (let match of matches) {
                // look for any dos or donts before the next match, last one wins.
                const nextMatchIndex = match.indices!![0][0]

                var substr = line.substring(matchIndex, nextMatchIndex);
                var lastDo = substr.lastIndexOf('do()');
                var lastDont = substr.lastIndexOf('don\'t()');
                if (lastDo > -1 && lastDo > lastDont) {
                    enabled = true;
                } else if (lastDont > -1 && lastDont > lastDo) {
                    enabled = false;
                }

                if (enabled) {
                    const product = parseInt(match[1]) * parseInt(match[2]);

                    // console.log(`match: ${match[0]} - ${match[1]} ${match[2]} = ${product}`)
                    sum = sum + BigInt(product)
                }
                matchIndex = nextMatchIndex;
            };
        } else {
            console.log('No mul found')
        }
    });
    console.log(`sum: ${sum}`)
}

part2();
