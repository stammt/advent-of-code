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
