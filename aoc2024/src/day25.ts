import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day25", true);

function part1() {
  const locks: number[][] = [];
  const keys: number[][] = [];

  let isLock = false;
  let isKey = false;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i] === "#####") {
      isLock = true;
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
      isKey = true;
      isLock = true;
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
}

function part2() {}

part1();
