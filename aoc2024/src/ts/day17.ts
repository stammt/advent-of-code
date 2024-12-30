import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day17", false);

type ComputerState = {
  a: bigint;
  b: bigint;
  c: bigint;
  pos: number;
  output: number[];
};

function evalCombo(op: bigint, state: ComputerState): bigint {
  if (op <= 3) return op;
  switch (op) {
    case 4n:
      return state.a;
    case 5n:
      return state.b;
    case 6n:
      return state.c;
  }
  return -1n;
}

function adv(comboOp: bigint, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  const result = BigInt(state.a) / BigInt(2) ** BigInt(op);
  //   console.log(`adv: op=${op}, result=${result}`);
  state.a = result;
  state.pos += 2;
}

function bxl(op: bigint, state: ComputerState) {
  state.b = state.b ^ op;
  state.pos += 2;
}

function bst(comboOp: bigint, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  state.b = op % 8n;
  state.pos += 2;
}

function jnz(op: bigint, state: ComputerState) {
  if (state.a !== 0n) {
    // console.log(`jnz moving to ${op}`);
    state.pos = Number(op);
  } else {
    // console.log(`jnz no-op`);
    state.pos += 2;
  }
}

function bxc(op: bigint, state: ComputerState) {
  state.b = state.b ^ state.c;
  state.pos += 2;
}

function out(comboOp: bigint, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  const result = op % 8n;
  //   console.log(`out ${op} : ${result}`);
  state.output.push(Number(result));
  state.pos += 2;
}

function bdv(comboOp: bigint, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  const result = BigInt(state.a) / BigInt(2) ** BigInt(op);
  state.b = result;
  state.pos += 2;
}

function cdv(comboOp: bigint, state: ComputerState) {
  const op = evalCombo(comboOp, state);
  const result = BigInt(state.a) / BigInt(2) ** BigInt(op);
  state.c = result;
  state.pos += 2;
}

const instructions = new Map<
  number,
  (op: bigint, state: ComputerState) => void
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

function printState(state: ComputerState) {
  console.log(
    `a: ${state.a}, b: ${state.b}, c: ${state.c} ; pos: ${state.pos} ; output: ${state.output}`
  );
}

function part1() {
  const state: ComputerState = {
    a: BigInt(lines[0].split(": ")[1]),
    b: BigInt(lines[1].split(": ")[1]),
    c: BigInt(lines[2].split(": ")[1]),
    pos: 0,
    output: [],
  };
  const program = lines[4]
    .split(": ")[1]
    .split(",")
    .map((e) => parseInt(e));

  console.log(`Initial state; `);
  printState(state);
  console.log(`Program: ${program}`);

  while (state.pos < program.length) {
    const i = program[state.pos];
    const op = BigInt(program[state.pos + 1]);
    instructions.get(i)!(op, state);
    printState(state);
  }

  console.log(`output: ${state.output}`);
}

function part2() {
  const initialState: ComputerState = {
    a: BigInt(lines[0].split(": ")[1]),
    b: BigInt(lines[1].split(": ")[1]),
    c: BigInt(lines[2].split(": ")[1]),
    pos: 0,
    output: [],
  };
  const program = lines[4]
    .split(": ")[1]
    .split(",")
    .map((e) => parseInt(e));

  console.log(`Initial state:`);
  printState(initialState);
  console.log(`Program: ${program}`);
  // for (let i = 50000000000001n; i < 300000000000000n; i++) {

  let base = 36000001000000n;
  const ones: number[] = [];
  const twos: number[] = [];

  for (let i = base; i < base + 500n; i++) {
    // console.log(`\n\n******* i=${i} ********`);
    const state: ComputerState = {
      a: BigInt(i),
      b: BigInt(initialState.b),
      c: BigInt(initialState.c),
      pos: 0,
      output: [],
    };
    let stop = false;
    while (!stop && state.pos < program.length) {
      const instruction = program[state.pos];
      const op = BigInt(program[state.pos + 1]);
      instructions.get(instruction)!(op, state);

      // for (let p = 0; p < program.length; p++) {
      //   if (state.output.length > p && state.output[p] !== program[p]) {
      //     //   console.log(`stopping, ${state.output} can't match ${program}`);
      //     stop = true;
      //   }
      // }
    }
    // I hate typescript...
    if (`${state.output}` === `${program}`) {
      console.log(`Found it! ${i}`);
      printState(state);
      break;
    } else {
      //if (i % 1000000n === 0n) {
      console.log(`Halted at i=${i} with `);
      ones.push(state.output[0]);
      if (twos.length === 0 || twos[twos.length - 1] !== state.output[1]) {
        twos.push(state.output[1]);
      }
      printState(state);
    }
  }

  console.log(`${ones}\n`);
  console.log(`${twos}`);
  // for (let x = 0; x < ones.length; x++) {
  //   console.log(`${ones[x]}   ${twos[x]}`);
  // }
  //   console.log(`output: ${state.output}`);
}

part2();

// i=120000000000000: 7,7,7,7,3,2,5,0,0,5,0,7,7,6,2,4
// i=120000001000000: 7,3,7,7,4,7,2,6,0,5,0,7,7,6,2,4
// i=130000000000000: 7,7,7,7,1,6,4,6,2,5,3,3,4,4,3,4
// i=130000001000000: 7,3,7,7,5,5,3,7,2,5,3,3,4,4,3,4

// i=150000001000000 7,3,7,7,0,2,7,0,3,0,3,1,0,7,1,3
// i=130000001000000 7,3,7,7,5,5,3,7,2,5,3,3,4,4,3,4
// i=100000001000000 7,3,7,7,3,0,1,7,7,1,5,7,6,1,1,5
// i=90000001000000  7,3,7,7,3,0,2,7,5,3,6,4,3,4,3,5
// i=80000001000000  7,3,7,7,1,3,7,3,0,1,7,7,7,7,7,5
// i=70000001000000  7,3,7,7,6,4,1,7,0,1,3,7,2,1,0,7
// i=50000001000000  7,3,7,7,0,3,0,5,3,7,2,6,3,6,6,7
// i=10000001000000  7,3,7,7,1,4,7,0,1,7,7,7,7,7,5
// i=40000001000000  7,3,7,7,7,0,5,2,7,0,7,7,5,3,7,7
// i=35000001000000  7,3,7,7,0,7,3,3,7,1,1,0,5,0,0
// i=36000001000000  7,3,7,7,3,6,7,2,7,6,3,1,6,7,3,7
// i=37000001000000  7,3,7,7,7,7,2,7,2,3,6,0,6,4,3,7
// 2,4,1,1,7,5,0,3,4,3,1,6,5,5,3,0
