from aoc_utils import splitInts

OP_HALT = 99
OP_ADD = 1
OP_MUL = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LT = 7
OP_EQ = 8

MODE_POSITION = 0
MODE_IMMEDIATE = 1

STATE_NOT_STARTED = -1
STATE_RUNNING = 0
STATE_HALTED = 1
STATE_WAITING_INPUT = 2

class Intcode:
    def __init__(self, memory):
        self.memory = memory
        self.i = 0
        self.output = []
        self.state = STATE_NOT_STARTED

    # Runs the program until it either halts or consumes all of the input and is waiting for more.
    def run_with_input(self, input: list[int]):
        self.output, self.state, self.i = run_intcode(self.memory, input, self.i)

    

# Parse an op into a tuple of (opcode, list of modes) where mode 0 is position, 1 is immediate.
# If there are fewer modes than parameters for this op, they are assumed to be 0.
def parse_op(op: int) -> tuple[int, list[int]]:
    opcode = op % 100
    op //= 100
    modes = []
    while op > 0:
        modes.append(op % 10)
        op //= 10
    return (opcode, modes)

def param_value(pos: int, i: int, modes: list[int], ints: list[int]) -> int:
    mode = 0 if len(modes) <= pos else modes[pos]
    return ints[ints[i+pos+1]] if mode == MODE_POSITION else ints[i+pos+1]

def run_intcode(ints: list[int], inputs: list[int], i = 0) -> tuple[list[int], int, int]:
    outputs = []
    state = STATE_RUNNING
    while True:
        opcode, modes = parse_op(ints[i])
        if opcode == OP_HALT:
            state = STATE_HALTED
            break
        elif opcode == OP_INPUT:
            if len(inputs) == 0:
                state = STATE_WAITING_INPUT
                break
            ints[ints[i+1]] = inputs.pop(0)
            i += 2
        elif opcode == OP_OUTPUT:
            op = param_value(0, i, modes, ints)
            outputs.append(op)
            i += 2
        elif opcode == OP_JUMP_IF_TRUE:
            p1 = param_value(0, i, modes, ints)
            p2 = param_value(1, i, modes, ints)
            if p1 != 0:
                i = p2
            else:
                i += 3
        elif opcode == OP_JUMP_IF_FALSE:
            p1 = param_value(0, i, modes, ints)
            p2 = param_value(1, i, modes, ints)
            if p1 == 0:
                i = p2
            else:
                i += 3
        elif opcode == OP_LT:
            p1 = param_value(0, i, modes, ints)
            p2 = param_value(1, i, modes, ints)
            ints[ints[i+3]] = 1 if p1 < p2 else 0
            i += 4
        elif opcode == OP_EQ:
            p1 = param_value(0, i, modes, ints)
            p2 = param_value(1, i, modes, ints)
            ints[ints[i+3]] = 1 if p1 == p2 else 0
            i += 4
        elif opcode in {OP_ADD, OP_MUL}:
            op1 = param_value(0, i, modes, ints)
            op2 = param_value(1, i, modes, ints)
            val = op1 + op2 if opcode == OP_ADD else op1 * op2
            ints[ints[i+3]] = val
            i += 4
    return (outputs, state, i)


