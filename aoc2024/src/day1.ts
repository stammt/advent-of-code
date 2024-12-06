import {readFileSync} from 'fs';

let data = readFileSync('input/day1.txt', 'utf-8')

let lines = data.split('\n')

let first = lines.map(e => parseInt(e.split(/\s+/)[0]))
let second = lines.map(e => parseInt(e.split(/\s+/)[1]))

function part1() {
    first.sort();
    second.sort();
    
    var sum = BigInt(0)
    for (let i = 0; i < lines.length; i++) {
        let dist = Math.abs(first[i] - second[i])
        sum = sum + BigInt(dist)
    }
    console.log(`sum: ${sum}`)
}

function part2() {
    const counts = second.reduce(function (acc, curr) {
        return acc[curr] ? ++acc[curr] : acc[curr] = 1, acc
      }, {});

    var score = 0
    for (let i = 0; i < first.length; i++) {
        const e = first[i];
        const count = (counts[e] || 0)
        score += (e * count)
    }
    console.log(`score: ${score}`)
}

part2();
