// Generate all combinations of ops that are length len.
export function combinations(ops: string[], len: number): string[][] {
  const result = new Array<string[]>();

  for (let i = 0; i < ops.length; i++) {
    const prefix = [ops[i]];
    if (len === 1) {
      result.push(prefix);
    } else {
      const suffixes = combinations(ops, len - 1);
      suffixes.forEach((element) => {
        result.push(prefix.concat(element));
      });
    }
  }
  return result;
}

export function stringPermutations(str: string): string[] {
  if (str.length <= 2) return str.length === 2 ? [str, str[1] + str[0]] : [str];
  return str
    .split("")
    .reduce(
      (acc, letter, i) =>
        acc.concat(
          stringPermutations(str.substring(0, i) + str.substring(i + 1)).map(
            (val) => letter + val
          )
        ),
      []
    );
}

export function getSubsets<T>(arr: T[]): T[][] {
  const result: T[][] = [];

  function backtrack(index: number, subset: T[]) {
    result.push([...subset]);

    for (let i = index; i < arr.length; i++) {
      subset.push(arr[i]);
      backtrack(i + 1, subset);
      subset.pop();
    }
  }

  backtrack(0, []);
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
