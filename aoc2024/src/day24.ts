import { Grid, linesToCharGrid, toNumberGrid } from "./utils/char-grid";
import { getSection, readInput } from "./utils/file-utils";
import { CardinalDirection, Point } from "./utils/point";
import { allPairs, combinations } from "./utils/utils";

const lines = readInput("day24", true);

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

function getInputAsDecimal(c: string, inputs: Map<string, boolean>): number {
  const labels = new Array<string>();
  inputs.forEach((v, k) => {
    if (k.startsWith(c)) {
      labels.push(k);
    }
  });
  labels.sort();
  const values = new Array<number>();
  labels.forEach((l) => values.push(inputs.get(l) ? 1 : 0));
  return parseInt(values.reverse().join(""), 2);
}

function getInputAsBits(c: string, inputs: Map<string, boolean>): number[] {
  const labels = new Array<string>();
  inputs.forEach((v, k) => {
    if (k.startsWith(c)) {
      labels.push(k);
    }
  });
  labels.sort();
  const values = new Array<number>();
  labels.forEach((l) => values.push(inputs.get(l) ? 1 : 0));
  return values;
}

function getOutput(gates: Gate[], inputInputs: Map<string, boolean>): number[] {
  // make a local copy to modify
  const inputs = new Map<string, boolean>(inputInputs);

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
        console.log(
          `${gate}: ${input1Value} ${gate.op} ${input2Value} is ${outputValue} to ${gate.output}`
        );
        if (zIndex !== -1) {
          zOutputValues[zIndex] = outputValue ? 1 : 0;
        }
      }
    });
  }

  console.log(zOutputs);
  console.log(zOutputValues);

  return zOutputValues;
}

function part2() {
  const inputs = parseInputs(getSection(0, lines));
  const gates = parseGates(getSection(1, lines));

  // first read all x,y values and see what z should be
  //   const x = getInputAsDecimal("x", inputs);
  //   const y = getInputAsDecimal("y", inputs);
  //   const z = x + y;
  //   const zExpectedValues = z
  //     .toString(2)
  //     .split("")
  //     .reverse()
  //     .map((e) => parseInt(e));
  //   console.log(`x=${x}, y=${y}, z=${z} ${zExpectedValues}`);

  const x = getInputAsBits("x", inputs);
  const y = getInputAsBits("y", inputs);
  const zExpectedValues = new Array<number>(); // 000101
  for (let i = 0; i < x.length; i++) {
    zExpectedValues.push(x[i] === 1 && y[i] === 1 ? 1 : 0);
  }
  const zOutputValues = getOutput(gates, inputs); // 100100

  console.log(x);
  console.log(y);
  console.log(zExpectedValues);
  console.log(zOutputValues);

  // gates outputting zero who want to output one
  const zerosToSwap = new Array<string>();
  // gates outputting one who want to output zero
  const onesToSwap = new Array<string>();

  // start at the z output level, see if we can swap enough of the gates.
  // if not, start tracing back to gates that feed that level, and so on.
  for (let i = 0; i < zOutputValues.length; i++) {
    if (zOutputValues[i] != zExpectedValues[i]) {
      if (zOutputValues[i] === 0) {
        zerosToSwap.push(`z${i.toString().padStart(2, "0")}`);
      } else {
        onesToSwap.push(`z${i.toString().padStart(2, "0")}`);
      }
    }
  }

  console.log(zerosToSwap);
  console.log(onesToSwap);

  /*******
  const zBadOutputLabels = new Array<string>();
  console.log(`${zExpectedValues.length} vs ${zOutputValues.length}`);
  for (let i = 0; i < zExpectedValues.length; i++) {
    if (zOutputValues[i] !== zExpectedValues[i]) {
      //   console.log(`bit ${i} is different`);
      zBadOutputLabels.push(`z${i}`);
    }
  }

  // track back from the outputs that are wrong to get the set of gates that might
  // need to be swapped.
  //   const gatesToSwap = new Array<Gate>();
  const inputsToSwap = new Set(zBadOutputLabels);
  const q = Array.from(zBadOutputLabels);
  while (q.length !== 0) {
    const z = q.pop();
    for (let i = 0; i < gates.length; i++) {
      if (gates[i].output === z) {
        inputsToSwap.add(gates[i].input1);
        inputsToSwap.add(gates[i].input2);
        q.push(gates[i].input1);
        q.push(gates[i].input2);
      }
    }
  }

  const allInputs = new Set();
  gates.forEach((g) => {
    allInputs.add(g.output);
    allInputs.add(g.input1);
    allInputs.add(g.input2);
  });

  console.log(`found ${inputsToSwap.size} out of ${allInputs.size}`);

  //   // brute force - get all pairs of gates; then all combinations of 4 pairs; and see if
  //   // swapping them gives the right output.
  //   const gatePairs = allPairs(gates);
  //   console.log(`pairs: ${gatePairs.length}`);
  //   const pairCombos = combinations(gatePairs, 4);

  //   console.log(
  //     `created ${gatePairs} pairs, for ${pairCombos} combinations to try`
  //   );
  //   pairCombos
  *******/
}

part2();
