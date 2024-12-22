import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";
import { allOrderings, stringPermutations } from "./utils/utils";

const lines = readInput("day21", true);

const UP = "^";
const DOWN = "v";
const LEFT = "<";
const RIGHT = ">";
const ACTIVATE = "A";
const INVALID = "#";

const keypad = linesToCharGrid(["789", "456", "123", "#0A"]);

const dirpad = linesToCharGrid(["#^A", "<v>"]);

function buildMoves(
  seq: string,
  fromPad: Grid<string>,
  toPad: Grid<string>,
  startPos: Point
): Set<string> {
  let moves: string[] = [];

  // for each char in the sequence, find the sequence to get it there
  let fromPos = startPos;
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
    const x = stringPermutations(stepMoves.join(""));
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
    // console.log(`orderings of ${moves}: ${x.join(" ** ")}`);
    // moves.push(ACTIVATE);
  }
  const moveSet = new Set<string>();
  moves.forEach((m) => moveSet.add(m));

  return moveSet;
}

function keepShortest(moves: Set<string>): Set<string> {
  let shortest = Infinity;
  moves.forEach((m) => {
    if (m.length < shortest) {
      shortest = m.length;
    }
  });
  const results = new Set<string>();
  moves.forEach((m) => {
    if (m.length === shortest) results.add(m);
  });
  return results;
}

function logMoves(moves: string) {
  console.log(`${moves.length} : ${moves}`);
}

function part1() {
  const seq = "029A";
  const startPos = new Point(2, 3);

  // Find all moves that would accomplish this sequence, then find the shortest
  // move length and get all sequences of moves of that length
  const moves = buildMoves(seq, dirpad, keypad, startPos);
  const shortestMoves = keepShortest(moves);

  shortestMoves.forEach((m) => logMoves(m));

  // repeat for the next two levels
  const dirStartPos = new Point(2, 0);
  const l2Moves = new Set<string>();
  shortestMoves.forEach((m) => {
    const theseMoves = buildMoves(m, dirpad, dirpad, dirStartPos);
    theseMoves.forEach((l2m) => l2Moves.add(l2m));
  });
  const l2ShortestMoves = keepShortest(l2Moves);
  console.log(`level 2`);
  l2ShortestMoves.forEach((m) => logMoves(m));

  const l3Moves = new Set<string>();
  l2ShortestMoves.forEach((m) => {
    const theseMoves = buildMoves(m, dirpad, dirpad, dirStartPos);
    theseMoves.forEach((l3m) => l2Moves.add(l3m));
  });
  const l3ShortestMoves = keepShortest(l3Moves);
  // const l3Moves = buildMoves(l2Moves, dirpad, dirpad, dirStartPos);
  console.log(`level 3`);

  l3ShortestMoves.forEach((m) => logMoves(m));
}

function part2() {}

part1();
