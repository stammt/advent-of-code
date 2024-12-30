import { readInput, getSection } from "./utils/file-utils";

const lines = readInput("day5", false);
const rules = getSection(0, lines);
const updates = getSection(1, lines);

// map of page number to the numbers that must be before it
const ruleMap = new Map<number, number[]>();
// map of page number to the numbers that must be after it
const afterRuleMap = new Map<number, number[]>();
rules.forEach((rule) => {
  const [val, before] = rule.split("|").map((e) => parseInt(e));
  if (ruleMap.has(val)) {
    ruleMap.set(val, ruleMap.get(val)!.concat([before]));
  } else {
    ruleMap.set(val, [before]);
  }

  if (afterRuleMap.has(before)) {
    afterRuleMap.set(before, afterRuleMap.get(before)!.concat([val]));
  } else {
    afterRuleMap.set(before, [val]);
  }
});

function part1() {
  let sum = 0;
  updates.forEach((update) => {
    const pages = update.split(",").map((e) => parseInt(e));
    let valid = true;
    for (let i = 0; i < pages.length; i++) {
      const rule = ruleMap.get(pages[i]);
      if (rule) {
        const after = pages.slice(0, i + 1);
        for (let j = 0; j < rule.length; j++) {
          if (after.indexOf(rule[j]) > -1) {
            // console.log(`Broke rule ${pages[i]} | ${rule} for ${update}`)
            valid = false;
            break;
          }
        }
      }
      if (!valid) {
        break;
      }
    }
    console.log(`valid ${valid} for ${update}`);
    if (valid) {
      const mid = Math.floor(pages.length / 2);
      const midValue = pages[mid];
      sum += midValue;
    }
  });
  console.log(`sum: ${sum}`);
}

// Return true if a is before b
function isBefore(a: number, b: number): boolean {
  if (!ruleMap.has(a)) return false;
  return ruleMap.get(a)!.includes(b);
}

// Return true if a is after b
function isAfter(a: number, b: number): boolean {
  if (!afterRuleMap.has(a)) return false;
  return afterRuleMap.get(a)!.includes(b);
}

function comparePages(a: number, b: number): number {
  if (isBefore(a, b)) return -1;
  else if (isAfter(a, b)) return 1;
  else return 0;
}

function isSameOrder(a: number[], b: number[]): boolean {
  return a.every((element, index) => {
    return element === b[index];
  });
}

function part2() {
  let sum = 0;
  updates.forEach((update) => {
    const pages = update.split(",").map((e) => parseInt(e));
    const sortedPages = Array.from(pages).sort(comparePages);
    if (!isSameOrder(pages, sortedPages)) {
      // console.log(`not valid, re-sorted (${pages}) to (${sortedPages})`)
      const mid = Math.floor(sortedPages.length / 2);
      const midValue = sortedPages[mid];
      sum += midValue;
    }
  });
  console.log(`sum: ${sum}`);
}

part2();
