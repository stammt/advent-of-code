import {readFileSync} from 'fs';

export function readInput(name: String, sample: Boolean = false) : String[] {
    const suffix = sample ? '-sample' : '';
    const data = readFileSync(`input/${name}${suffix}.txt`, 'utf-8');
    return data.split('\n');
}