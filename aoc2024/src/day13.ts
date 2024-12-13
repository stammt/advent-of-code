import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput, splitOnEmptyLines } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day13", false);

function parseButton(button: string): Point {
  const steps = button.split(": ")[1];
  const [x, y] = steps.split(", ");
  const dx = parseInt(x.split("+")[1]);
  const dy = parseInt(y.split("+")[1]);
  return new Point(dx, dy);
}
function parsePrize(button: string): Point {
  const steps = button.split(": ")[1];
  const [x, y] = steps.split(", ");
  const dx = parseInt(x.split("=")[1]);
  const dy = parseInt(y.split("=")[1]);
  return new Point(dx, dy);
}

function part1() {
  const aPrice = 3;
  const bPrice = 1;
  const sections = splitOnEmptyLines(lines);

  let totalCost = 0;
  let winnerCount = 0;
  sections.forEach((section) => {
    const a = parseButton(section[0]);
    const b = parseButton(section[1]);
    const prize = parsePrize(section[2]);

    console.log(`${prize} : ${a} ${b}`);

    let minCost: number;

    // (a.x * na) + (b.x * nb) = prize.x
    // (a.y * na) + (b.y * nb) = prize.y
    for (let na = 0; na < 100; na++) {
      // nb = (prize.x - (a.x * na)) / b.x
      const bx = prize.x - a.x * na;
      if (bx % b.x === 0) {
        const nb = bx / b.x;
        if (nb * b.y === prize.y - a.y * na) {
          // we have a winner!
          const cost = aPrice * na + bPrice * nb;
          console.log(`Winner ${prize} with ${na}, ${nb} costs ${cost}`);
          if (!minCost || cost < minCost) {
            minCost = cost;
          }
        }
      }
    }
    if (minCost) {
      winnerCount++;
      console.log(`minCost of ${prize} is ${minCost}`);
      totalCost += minCost;
    }
  });
  console.log(`total cost: ${totalCost} for ${winnerCount} winners`);
}

function part2() {}

part1();
