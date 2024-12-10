import { readInput } from "./utils/file-utils";

const lines = readInput("day9", false);

type Block = {
  fileId: number;
  fileSize: number;
  freeSpace: number;
};

function parseLine(line: string): Block[] {
  const results = new Array<Block>();
  let fileId = 0;
  for (let i = 0; i < line.length; i++) {
    const fileSize = parseInt(line[i]);
    const freeSpace = i < line.length - 1 ? parseInt(line[i + 1]) : 0;
    results.push({ fileId: fileId, fileSize: fileSize, freeSpace: freeSpace });
    i++;
    fileId++;
  }
  return results;
}

function printBlock(block: Block): string {
  let result = "";
  for (let i = 0; i < block.fileSize; i++) {
    result += `${block.fileId}`;
  }
  for (let i = 0; i < block.freeSpace; i++) {
    result += ".";
  }
  return result;
}

function printBlocks(blocks: Block[]): string {
  let result = "";
  for (let i = 0; i < blocks.length; i++) {
    result += printBlock(blocks[i]);
  }
  return result;
}

function checksum(blocks: Block[]): bigint {
  let result = BigInt(0);

  let position = 0;
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];
    for (let p = 0; p < block.fileSize; p++) {
      result += BigInt(position * block.fileId);
      position++;
    }
    position += block.freeSpace;
  }
  return result;
}

function part1() {
  const blocks = parseLine(lines[0]);
  console.log(printBlocks(blocks));

  let fromEnd = 0;
  let done = false;
  while (!done) {
    const i = blocks.length - 1 - fromEnd;
    console.log(`fromEnd: ${fromEnd}, i ${i}, blocks length: ${blocks.length}`);
    if (i < 0) break;

    const block = blocks[i];
    while (block.fileSize > 0) {
      // find the first node with free space
      const firstFreeIndex = blocks.findIndex((e) => e.freeSpace > 0);
      if (firstFreeIndex >= blocks.indexOf(block)) {
        console
          .log
          //   `firstFreeIndex: ${firstFreeIndex}, i: ${i} is ${printBlock(block)}`
          ();
        done = true;
        break;
      }
      const firstFreeBlock = blocks[firstFreeIndex];
      // If it's the same file, just append to it.
      // Otherwise insert a new block.
      if (firstFreeBlock.fileId === block.fileId) {
        block.fileSize--;
        block.freeSpace++;
        firstFreeBlock.fileSize++;
        firstFreeBlock.freeSpace--;
      } else {
        const moved: Block = {
          fileId: block.fileId,
          fileSize: 1,
          freeSpace: firstFreeBlock.freeSpace - 1,
        };
        block.freeSpace++;
        block.fileSize--;
        firstFreeBlock.freeSpace = 0;
        blocks.splice(firstFreeIndex + 1, 0, moved);
      }
      //   console.log(printBlocks(blocks));
    }
    fromEnd++;
  }
  console.log(`checksum: ${checksum(blocks)}`);
}

function part2() {
  const blocks = parseLine(lines[0]);
  console.log(printBlocks(blocks));

  let fileId = blocks[blocks.length - 1].fileId;
  while (fileId > 0) {
    const blockIndex = blocks.findIndex((e) => e.fileId === fileId)!;
    const block = blocks[blockIndex];

    // find the first node with enough free space
    const firstFreeIndex = blocks.findIndex(
      (e) => e.freeSpace >= block.fileSize
    );
    // don't try to move to the right
    if (firstFreeIndex < blockIndex) {
      const firstFreeBlock = blocks[firstFreeIndex];
      if (firstFreeBlock) {
        const moved: Block = {
          fileId: block.fileId,
          fileSize: block.fileSize,
          freeSpace: firstFreeBlock.freeSpace - block.fileSize,
        };
        firstFreeBlock.freeSpace = 0;
        block.freeSpace += block.fileSize;
        block.fileSize = 0;
        blocks.splice(firstFreeIndex + 1, 0, moved);
        // console.log(printBlocks(blocks));
      }
    }
    fileId--;
  }
  console.log(`checksum: ${checksum(blocks)}`);
}

part2();
