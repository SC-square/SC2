# from instructions.Instruction import Instruction


class Code:
    '''
    private class
    '''

    def __init__(self, code: dict) -> None:
        self._code = code  # dict{int:Instruction}
        self._size = None
        self.__selfOrdered()
        self.__setSize()

    def __selfOrdered(self):
        self._code = dict(sorted(self._code.items()))

    def __setSize(self):
        if len(self._code):
            lastOffset, lastInstruction = list(self._code.items())[-1]
            self._size = lastOffset + lastInstruction.getSize
        else:
            self._size = 0

    def __iter__(self):
        return iter(self._code.items())

    @property
    def getSize(self):
        return self._size

    def get(self, offset: int):  # -> Instruction
        return self._code.get(offset, None)

    def getList(self) -> list:
        return list(self._code.values())

    def toBinaryString(self) -> str:
        binary = ''
        for instruction in self.getList():
            binary += instruction.toBinaryString()
        return binary

    def getOpcodeSequence(self, includeOperand: bool = False) -> list:
        opcodes = []
        for instruction in self.getList():
            opcodes.append(instruction.getOpcode)
            if includeOperand and instruction.hasOperand:
                opcodes.append(instruction.getOperand)
        return opcodes
