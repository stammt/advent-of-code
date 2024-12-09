import {readFileSync} from 'fs';

export function readInput(name: String, sample: Boolean = false) : string[] {
    const suffix = sample ? '-sample' : '';
    const data = readFileSync(`input/${name}${suffix}.txt`, 'utf-8');
    return data.split('\n');
}

export function getSection(index: number, lines: string[]) : string[] {
    const results = new Array<string>();

    let section = 0;
    lines.forEach(line => {
        if (line.trim().length === 0) {
            section++;
        } else if (section === index) {
            results.push(line);
        }
    });

    return results;
}