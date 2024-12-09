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
