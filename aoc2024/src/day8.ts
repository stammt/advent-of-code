import { isOnTheGrid, iterateGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { Point } from "./utils/point";
import { allPairs } from "./utils/utils";

const lines = readInput("day8", false);

function buildAntennas(): Map<string, Point[]> {
  // build a map of frequency id to list of positions for those frequencies
  const antennas = new Map<string, Point[]>();

  iterateGrid(lines, (x, y, c) => {
    if (c !== ".") {
      if (antennas.has(c)) {
        antennas.get(c)!.push(new Point(x, y));
      } else {
        antennas.set(c, [new Point(x, y)]);
      }
    }
  });
  return antennas;
}

function part1() {
  const antennas = buildAntennas();
  const uniqueNodes = new Set<string>();
  antennas.forEach((points, freq) => {
    const pairs = allPairs(points);
    for (let i = 0; i < pairs.length; i++) {
      const pair = pairs[i];
      const dx = pair.a.x - pair.b.x;
      const dy = pair.a.y - pair.b.y;

      const node1 = new Point(pair.a.x + dx, pair.a.y + dy);
      const node2 = new Point(pair.b.x - dx, pair.b.y - dy);

      if (isOnTheGrid(node1, lines)) {
        uniqueNodes.add(node1.toString());
        // console.log(`Found node for ${freq}: ${node1}`);
      }
      if (isOnTheGrid(node2, lines)) {
        uniqueNodes.add(node2.toString());
        // console.log(`Found node for ${freq}: ${node2}`);
      }
    }
  });

  console.log(`node count: ${uniqueNodes.size}`);
}

function part2() {
  const antennas = buildAntennas();
  const uniqueNodes = new Set<string>();
  antennas.forEach((points, freq) => {
    const pairs = allPairs(points);
    for (let i = 0; i < pairs.length; i++) {
      const pair = pairs[i];
      const dx = pair.a.x - pair.b.x;
      const dy = pair.a.y - pair.b.y;

      // add the antennas themselves
      uniqueNodes.add(pair.a.toString());
      uniqueNodes.add(pair.b.toString());

      // walk in each direction until we leave the grid
      let node1 = new Point(pair.a.x + dx, pair.a.y + dy);
      while (isOnTheGrid(node1, lines)) {
        uniqueNodes.add(node1.toString());
        node1 = new Point(node1.x + dx, node1.y + dy);
      }

      let node2 = new Point(pair.b.x - dx, pair.b.y - dy);
      while (isOnTheGrid(node2, lines)) {
        uniqueNodes.add(node2.toString());
        node2 = new Point(node2.x - dx, node2.y - dy);
      }
    }
  });

  console.log(`node count: ${uniqueNodes.size}`);
}

part2();
