import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";
import { allOrderings, stringPermutations } from "./utils/utils";

const lines = readInput("day21", false);

const UP = "^";
const DOWN = "v";
const LEFT = "<";
const RIGHT = ">";
const ACTIVATE = "A";
const INVALID = "#";

const keypad = linesToCharGrid(["789", "456", "123", "#0A"]);

const dirpad = linesToCharGrid(["#^A", "<v>"]);

// return false if this would take us onto an invalid square
function validateMoves(
  startPos: Point,
  moves: string,
  pad: Grid<string>
): boolean {
  let p = startPos;
  for (let m = 0; m < moves.length; m++) {
    const dir =
      moves[m] === "^"
        ? CardinalDirection.N
        : moves[m] === "v"
          ? CardinalDirection.S
          : moves[m] === ">"
            ? CardinalDirection.E
            : CardinalDirection.W;
    p = p.step(dir);
    if (!pad.isValid(p) || pad.getValue(p) === INVALID) {
      // console.log(
      //   `moves not valid from ${startPos}: ${moves}: ${m} ${dir} ${pad.isValid(p)} ${pad.getValue(p)}`
      // );
      return false;
    }
  }
  return true;
}

function buildMoves(
  seq: string,
  toPad: Grid<string>,
  startPos: Point
): Set<string> {
  let moves: string[] = [];

  // for each char in the sequence, find the sequence to get it there
  let fromPos = startPos;
  let lastFromPos = fromPos;
  for (let i = 0; i < seq.length; i++) {
    const c = seq[i];
    const toPos = toPad.find(c);
    const stepMoves = [];
    while (!toPos.equals(fromPos)) {
      let move: string;
      if (fromPos.x > toPos.x) {
        const next = fromPos.step(CardinalDirection.W);
        if (toPad.isValid(next) && toPad.getValue(next) !== INVALID) {
          fromPos = next;
          move = LEFT;
        }
      }
      if (!move && fromPos.x < toPos.x) {
        const next = fromPos.step(CardinalDirection.E);
        if (toPad.isValid(next) && toPad.getValue(next) !== INVALID) {
          fromPos = next;
          move = RIGHT;
        }
      }
      if (!move && fromPos.y > toPos.y) {
        const next = fromPos.step(CardinalDirection.N);
        if (toPad.isValid(next) && toPad.getValue(next) !== INVALID) {
          fromPos = next;
          move = UP;
        }
      }
      if (!move && fromPos.y < toPos.y) {
        const next = fromPos.step(CardinalDirection.S);
        if (toPad.isValid(next) && toPad.getValue(next) !== INVALID) {
          fromPos = next;
          move = DOWN;
        }
      }
      stepMoves.push(move);
    }
    // generate all orderings of this move, and add to previous lists
    const x = stringPermutations(stepMoves.join("")).filter((e) =>
      validateMoves(lastFromPos, e, toPad)
    );
    if (moves.length === 0) {
      x.forEach((y) => {
        moves.push(y + ACTIVATE);
      });
    } else {
      const nextMoves: string[] = [];
      moves.forEach((prefix) => {
        x.forEach((y) => {
          nextMoves.push(prefix + y + ACTIVATE);
        });
      });
      moves = nextMoves;
    }
    lastFromPos = fromPos;
    // console.log(`orderings of ${moves}: ${x.join(" ** ")}`);
    // moves.push(ACTIVATE);
  }
  const moveSet = new Set<string>();
  moves.forEach((m) => moveSet.add(m));

  return moveSet;
}

// gets the first shortest entry we find
function keepShortest(moves: Set<string>): string[] {
  let shortest = Infinity;
  moves.forEach((m) => {
    if (m.length < shortest) {
      shortest = m.length;
    }
  });
  const results = Array<string>();
  moves.forEach((m) => {
    if (m.length === shortest) results.push(m);
  });
  return results;
}

function logMoves(moves: string) {
  console.log(`${moves.length} : ${moves}`);
}

function part1() {
  let complexitySum = 0;
  lines.forEach((seq) => {
    console.log(`\n### sequence ${seq}`);
    const startPos = new Point(2, 3); // A

    let lastPos = startPos;
    let sequenceLength = 0;

    // walk through the sequence one step at a time, finding the shortest moves
    // for each step.
    for (let i = 0; i < seq.length; i++) {
      // const nextPos = keypad.find(seq[i]);
      console.log(`*** moving from ${lastPos} to ${seq[i]}`);

      // Find all moves that would accomplish this sequence, then find the shortest
      // move length and get all sequences of moves of that length
      const moves = buildMoves(seq[i], keypad, lastPos);

      let shortestMoves = keepShortest(moves);
      // shortestMoves.forEach((m) => logMoves(m));

      // repeat for the next two levels
      for (let level = 0; level < 25; level++) {
        console.log(`level ${level} with ${shortestMoves.length} moves to try`);
        // dirpad always starts at "A", (2, 0);
        const dirStartPos = new Point(2, 0);

        const levelMoves = new Set<string>();
        shortestMoves.forEach((m) => {
          const theseMoves = buildMoves(m, dirpad, dirStartPos);
          theseMoves.forEach((l2m) => levelMoves.add(l2m));
        });
        shortestMoves = Array.from(keepShortest(levelMoves));
      }
      sequenceLength += shortestMoves[0].length;

      lastPos = keypad.find(seq[i]);
    }

    const complexity =
      sequenceLength * parseInt(seq.substring(0, seq.length - 1));
    console.log(
      `total length for ${seq}: ${sequenceLength}, complexity ${complexity}`
    );
    complexitySum += complexity;
  });
  console.log(`total complexity: ${complexitySum}`);
}

function part2() {
  let complexitySum = 0;

  // cache of move counts that it takes to move from one point to another on the
  // first dirpad, from the last dirpad.
  const moveCountCache = new Map<string, number>();

  lines.forEach((seq) => {
    console.log(`\n### sequence ${seq}`);
    const keypadStartPos = new Point(2, 3); // A on the keypad

    // Find all dirpad moves that would accomplish this sequence on the keypad, then find the shortest
    // move length and get all sequences of moves of that length
    const moves = buildMoves(seq, keypad, keypadStartPos);
    const shortestMoves = keepShortest(moves);

    // Then for each sequence of dirpad presses, expand out to the sequence of presses at the
    // last dirpad.
    const dirpadStartPos = new Point(2, 0);

    let shortestSequenceLength = Infinity;
    shortestMoves.forEach((m) => {
      let sequenceLength = 0;
      console.log(`looking at ${m}`);
      let dirpadPos = dirpadStartPos;
      for (let i = 0; i < m.length; i++) {
        const dirpadNextPos = dirpad.find(m[i]);
        const cacheKey = `${dirpadPos}:${dirpadNextPos}`;
        console.log(
          `Moving dirpad from ${dirpadPos} to ${dirpadNextPos} for ${m[i]}`
        );
        if (moveCountCache.has(cacheKey)) {
          console.log(
            `cache hit for ${cacheKey}: ${moveCountCache.get(cacheKey)}`
          );
          sequenceLength += moveCountCache.get(cacheKey)!;
        } else {
          // Build the moves for this level, then for each move see how many moves it expands
          // to for the next level, and trace/expand that down for all the levels.
          const levelMoves = buildMoves(m[i], dirpad, dirpadPos);
          const shortestLevelMoves = Array.from(keepShortest(levelMoves));

          // repeat for the next twenty-five levels

          let shortestLevelMoves: string[] = [m[i]];
          // repeat for the next two levels
          for (let level = 0; level < 25; level++) {
            const levelMoves = new Set<string>();
            shortestLevelMoves.forEach((slm) => {
              const theseMoves = buildMoves(
                slm,
                dirpad,
                level == 0 ? dirpadPos : dirpadStartPos
              );
              theseMoves.forEach((l2m) => levelMoves.add(l2m));
            });
            shortestLevelMoves = Array.from(keepShortest(levelMoves));
            // console.log(
            //   `using ${shortestLevelMoves[0].length}: ${shortestLevelMoves[0]}`
            // );
          }

          // console.log(
          //   `using ${shortestLevelMoves[0].length}: ${shortestLevelMoves[0]}`
          // );
          moveCountCache.set(cacheKey, shortestLevelMoves[0].length);
          sequenceLength += shortestLevelMoves[0].length;
        }
        dirpadPos = dirpadNextPos;
      }
      if (sequenceLength < shortestSequenceLength) {
        shortestSequenceLength = sequenceLength;
      }
    });

    const complexity =
      shortestSequenceLength * parseInt(seq.substring(0, seq.length - 1));
    console.log(
      `total length for ${seq}: ${shortestSequenceLength}, complexity ${complexity}`
    );
    complexitySum += complexity;
  });

  //593812 too low
  console.log(`total complexity: ${complexitySum}`);
}

part2();
