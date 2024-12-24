import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { getSection, readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";

const lines = readInput("day24", false);

type Gate = {
  input1: string;
  input2: string;
  op: string;
  output: string;
};

function parseInputs(inputs: string[]): Map<string, boolean> {
  const result = new Map<string, boolean>();
  inputs.forEach((input) => {
    const [name, value] = input.split(": ");
    result.set(name, value === "1");
  });
  return result;
}

function parseGates(gates: string[]): Gate[] {
  const result = new Array<Gate>();
  gates.forEach((gate) => {
    const [g, output] = gate.split(" -> ");
    const [input1, op, input2] = g.split(" ");
    result.push({ input1: input1, input2: input2, op: op, output: output });
  });
  return result;
}

function part1() {
  const inputs = parseInputs(getSection(0, lines));
  const gates = parseGates(getSection(1, lines));

  const zOutputs = new Array<string>();
  gates.forEach((gate) => {
    if (gate.output.startsWith("z")) {
      zOutputs.push(gate.output);
    }
  });
  zOutputs.sort();

  const zOutputValues = new Array<number>();
  for (let i = 0; i < zOutputs.length; i++) {
    zOutputValues.push(-1);
  }

  while (zOutputValues.includes(-1)) {
    const remainingGates = gates.filter((g) => !inputs.has(g.output));
    remainingGates.forEach((gate) => {
      if (inputs.has(gate.input1) && inputs.has(gate.input2)) {
        const input1Value = inputs.get(gate.input1)!;
        const input2Value = inputs.get(gate.input2)!;
        const outputValue =
          gate.op === "AND"
            ? input1Value && input2Value
            : gate.op === "OR"
              ? input1Value || input2Value
              : input1Value !== input2Value;
        inputs.set(gate.output, outputValue);

        const zIndex = zOutputs.indexOf(gate.output);
        if (zIndex !== -1) {
          zOutputValues[zIndex] = outputValue ? 1 : 0;
        }
      }
    });
  }

  const z = parseInt(zOutputValues.reverse().join(""), 2);
  console.log(`z=${z} : ${zOutputValues}`);
}

function part2() {}

part1();
