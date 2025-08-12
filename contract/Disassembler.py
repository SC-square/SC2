from instructions.InstructionTable import InstructionTable
from evm.Code import Code


class Disassembler:
    '''
    public static class
    '''
    @staticmethod
    def disassemble(binary: str) -> Code:
        if str(binary).startswith("0x"):
            binary = binary[2:]
        code = {}  # {offset: Instruction}
        i = 0
        while i < len(binary):
            j = i + 2
            opcodeStr = binary[i:j]
            opcode = int(opcodeStr, 16)
            offset = int(i / 2)
            instruction = InstructionTable.select(opcode, offset)
            i = j
            if instruction.hasOperand:
                j += instruction.getOperandSize * 2
                operandStr = binary[i:j]
                # if operandStr = ''
                operandInt = int(operandStr, 16) if len(operandStr) else 0
                instruction.setOperand(operandInt)
                i = j
            code[offset] = instruction
        return Code(code)
