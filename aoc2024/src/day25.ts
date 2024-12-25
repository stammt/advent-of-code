import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day25", false);

function part1() {
  const locks: number[][] = [];
  const keys: number[][] = [];

  for (let i = 0; i < lines.length; i++) {
    if (lines[i] === "#####") {
      const heights: number[] = [0, 0, 0, 0, 0];
      for (let j = i + 1; j < i + 6; j++) {
        for (let x = 0; x < 5; x++) {
          if (lines[j][x] === "#") {
            heights[x] = heights[x] + 1;
          }
        }
      }
      locks.push(heights);
      i = i + 7;
    } else if (lines[i] === ".....") {
      const heights: number[] = [0, 0, 0, 0, 0];
      for (let j = i + 5; j > i; j--) {
        for (let x = 0; x < 5; x++) {
          if (lines[j][x] === "#") {
            heights[x] = heights[x] + 1;
          }
        }
      }
      keys.push(heights);
      i = i + 7;
    }
  }

  console.log("locks:");
  console.log(locks.join("\n"));

  console.log("keys:");
  console.log(keys.join("\n"));

  let count = 0;
  for (let l = 0; l < locks.length; l++) {
    const lock = locks[l];
    for (let k = 0; k < keys.length; k++) {
      const key = keys[k];
      let fits = true;
      for (let x = 0; fits && x < key.length; x++) {
        if (key[x] + lock[x] > 5) {
          fits = false;
        }
      }
      if (fits) {
        count += 1;
      }
    }
  }
  console.log(`count: ${count}`);
}

function part2() {}

part1();
