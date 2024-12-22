// Generate all permutations of ops that are length len.
export function permutations(ops: string[], len: number): string[][] {
  const result = new Array<string[]>();

  for (let i = 0; i < ops.length; i++) {
    const prefix = [ops[i]];
    if (len === 1) {
      result.push(prefix);
    } else {
      const suffixes = permutations(ops, len - 1);
      suffixes.forEach((element) => {
        result.push(prefix.concat(element));
      });
    }
  }
  return result;
}

export function allOrderings(s: string): string[] {
  return allOrderingsInternal(s, s.length);
}

function allOrderingsInternal(s: string, len: number): string[] {
  const results: string[][] = [];
  for (let i = 0; i < s.length; i++) {
    const prefix = [s[i]];
    if (len === 1) {
      results.push(prefix);
    } else {
      const suffixes = allOrderingsInternal(s.substring(1), len - 1);
      suffixes.forEach((element) => {
        results.push(prefix.concat(element));
      });
    }
  }

  return results.map((r) => r.join(""));
}

// generate a list of all pairs of values in the given array
export function allPairs<T>(arr: T[]): { a: T; b: T }[] {
  const result = new Array<{ a: T; b: T }>();
  for (let i = 0; i < arr.length - 1; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      result.push({ a: arr[i], b: arr[j] });
    }
  }
  return result;
}
