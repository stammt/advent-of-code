import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";
import { allOrderings, permutations } from "./utils/utils";

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
): string {
  const moves: string[] = [];

  // for each char in the sequence, find the sequence to get it there
  let fromPos = startPos;
  for (let i = 0; i < seq.length; i++) {
    const c = seq[i];
    const toPos = toPad.find(c);
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
      moves.push(move);
    }
    // generate all orderings of this move, and add to previous lists
    const x = allOrderings(moves.join(""));
    console.log(`orderings of ${moves}: ${x.join(" ** ")}`);
    moves.push(ACTIVATE);
  }
  return moves.join("");
}

function logMoves(moves: string) {
  console.log(`${moves.length} : ${moves}`);
}

function part1() {
  const seq = "029A";
  const startPos = new Point(2, 3);
  const moves = buildMoves(seq, dirpad, keypad, startPos);

  logMoves(moves);

  const dirStartPos = new Point(2, 0);
  const l2Moves = buildMoves(moves, dirpad, dirpad, dirStartPos);
  logMoves(l2Moves);

  const l3Moves = buildMoves(l2Moves, dirpad, dirpad, dirStartPos);

  logMoves(l3Moves);
}

function part2() {}

part1();
