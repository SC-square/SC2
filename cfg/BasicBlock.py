from cfg.Node import Node
from instructions.Instruction import Instruction


class BasicBlock(Node):
    def __init__(self) -> None:
        super().__init__()
        self._startOffset = None
        self._endOffset = None
        self._instructions = []
        self._size = 0
        self._stackBalance = 0

    def __len__(self) -> int:
        return len(self._instructions)

    def __str__(self) -> str:
        return hex(self._name)

    @property
    def getStartOffset(self) -> int:
        return self._startOffset

    @property
    def getEndOffset(self) -> int:
        return self._endOffset

    @property
    def getInstructions(self) -> list:
        return self._instructions

    @property
    def getSize(self) -> int:
        return self._size

    @property
    def getStackBalance(self) -> int:
        return self._stackBalance

    @property
    def isOrphan(self) -> bool:
        return (not self.hasPredecessors) and (not self.hasSuccessors)

    def setStartOffset(self, startOffset: int):
        self._startOffset = startOffset
        self.setName(self._startOffset)

    def setEndOffset(self, endOffset: int):
        self._endOffset = endOffset

    def setInstructions(self, instructions: list):
        self._instructions = instructions

    def setSize(self, size: int):
        self._size = size

    def getNextOffset(self):
        return self.getStartOffset + self.getSize

    def addInstruction(self, instruction: Instruction) -> bool:
        if instruction not in self._instructions:
            # append instruction
            self._instructions.append(instruction)
            # update block size
            self._size += instruction.getSize
            # update start and end offset
            offset = instruction.getOffset
            if self._startOffset is None or offset < self._startOffset:
                self.setStartOffset(offset)
            if self._endOffset is None or offset > self._endOffset:
                self.setEndOffset(offset)
            self._stackBalance += instruction.getStackBalance
            return True
        return False

    def instructionsToString(self) -> str:
        # instructions = [str(i) for i in self._instructions]
        instructions = [i.toStringWithArgument() for i in self._instructions]
        return '\n'.join(instructions)

    def resetOffset(self, startOffset: int) -> int:
        '''
        reset all offsets of instructions based on the start offset; reset stack balance

        parameter: `startOffset`, the start offset of this block
        return: the start offset of next block
        '''
        nextOffset = startOffset
        stackBalance = 0
        for i in self._instructions:
            i.setOffset(nextOffset)
            nextOffset += i.getSize
            stackBalance += i.getStackBalance
        self.resetMeta()
        self._stackBalance = stackBalance
        return nextOffset

    def resetMeta(self):
        '''
        reset `name`, `startOffset`, `endOffset`, `size` 
        based on the first and last instructions
        '''
        startOffset = self._instructions[0].getOffset
        endOffset = self._instructions[-1].getOffset
        size = self._instructions[-1].getNextOffset() - startOffset
        self.setStartOffset(startOffset)
        self.setEndOffset(endOffset)
        self.setSize(size)

    def resetStackBalance(self):
        stackBalance = 0
        for i in self._instructions:
            stackBalance += i.getStackBalance
        self._stackBalance = stackBalance

    def toJson(self, simplified: bool = False, semantic: bool = False) -> dict:
        '''
        convert basic block to json according to EtherSolve format
        '''
        result = {}
        result["offset"] = self._startOffset
        result["length"] = self._size
        result["stackBalance"] = self._stackBalance
        if not simplified:
            result["bytecodeHex"] = ''.join(
                [i.toBinaryString() for i in self._instructions])
        if semantic:
            result["parsedOpcodes"] = '\n'.join(
                [i.toStringWithSemantic() for i in self._instructions])
        else:
            result["parsedOpcodes"] = '\n'.join(
                [str(i) for i in self._instructions])
        return result

    def loadFromJson(self, jsonDict: dict):
        # TODO:
        raise NotImplementedError("TBD")
        startOffset = jsonDict["offset"]
        parsedOpcodes = jsonDict["parsedOpcodes"]
        instructions = parsedOpcodes.split('\n')
        for i in instructions:
            pass

