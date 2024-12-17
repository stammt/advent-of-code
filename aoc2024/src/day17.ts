import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day17", false);

type ComputerState = {
  a: number;
  b: number;
  c: number;
  pos: number;
  output: number[];
};

function evalCombo(op: number, state: ComputerState): number {
  if (op <= 3) return op;
  switch (op) {
    case 4:
      return state.a;
    case 5:
      return state.b;
    case 6:
      return state.c;
  }
  return -1;
}

function adv(comboOp: number, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  const result = state.a / Math.pow(2, op);
  //   console.log(`adv: op=${op}, result=${result}`);
  state.a = Math.trunc(result);
  state.pos += 2;
}

function bxl(op: number, state: ComputerState) {
  state.b = state.b ^ op;
  state.pos += 2;
}

function bst(comboOp: number, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  state.b = op % 8;
  state.pos += 2;
}

function jnz(op: number, state: ComputerState) {
  if (state.a !== 0) {
    // console.log(`jnz moving to ${op}`);
    state.pos = op;
  } else {
    // console.log(`jnz no-op`);
    state.pos += 2;
  }
}

function bxc(op: number, state: ComputerState) {
  state.b = state.b ^ state.c;
  state.pos += 2;
}

function out(comboOp: number, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  console.log(`out: op=${op}`);
  state.output.push(op % 8);
  state.pos += 2;
}

function bdv(comboOp: number, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  const result = state.a / Math.pow(2, op);
  state.b = Math.trunc(result);
  state.pos += 2;
}

function cdv(comboOp: number, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  const result = state.a / Math.pow(2, op);
  state.c = Math.trunc(result);
  state.pos += 2;
}

const instructions = new Map<
  number,
  (op: number, state: ComputerState) => void
>([
  [0, adv],
  [1, bxl],
  [2, bst],
  [3, jnz],
  [4, bxc],
  [5, out],
  [6, bdv],
  [7, cdv],
]);

function part1() {
  const state: ComputerState = {
    a: parseInt(lines[0].split(": ")[1]),
    b: parseInt(lines[1].split(": ")[1]),
    c: parseInt(lines[2].split(": ")[1]),
    pos: 0,
    output: [],
  };
  const program = lines[4]
    .split(": ")[1]
    .split(",")
    .map((e) => parseInt(e));

  console.log(`Initial state; ${JSON.stringify(state)}`);
  console.log(`Program: ${program}`);

  while (state.pos < program.length) {
    const i = program[state.pos];
    const op = program[state.pos + 1];
    instructions.get(i)!(op, state);
    console.log(`state: ${JSON.stringify(state)}`);
  }

  console.log(`output: ${state.output}`);
}

function part2() {}

part1();
