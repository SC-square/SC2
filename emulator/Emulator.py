from contract.Disassembler import Disassembler
from evm.State import State
from emulator.EmulatorGUI import EmulatorGUI


class Emulator:
    def __init__(self, binary) -> None:
        self.code = Disassembler.disassemble(binary)
        self.height = 20
        self.width = 72

    def run(self):
        state = State(self.code)
        while True:
            i = state.getNext()
            if i is None:
                break
            self.__printState(state)
            command = input()
            if command == 'q':
                break
            i.execute(state)

    def __printState(self, state: State):
        EmulatorGUI.clearTerminal()
        instructionFrame = EmulatorGUI.singleFrame(
            self.__getInstructionList(state), self.width, title='Instructions')
        stackFrame = EmulatorGUI.singleFrame(
            state.stack.toStringList(), self.width, title='Stack')
        memoryFrame = EmulatorGUI.singleFrame(
            state.memory.toStringList(), self.width, title='Memory')
        gas = f"Gas: {state.gas}"
        output = []
        output.append(instructionFrame)
        output.append(stackFrame)
        output.append(memoryFrame)
        output.append(gas)
        print('\n'.join(output))

    def __getInstructionList(self, state: State):
        defaultMargin = 1
        defaultLength = 5
        indicator = '> '
        space = ' '
        length = defaultLength
        margin = defaultMargin if length > defaultMargin * 2 else 0
        instruction = state.getNext()
        fullList = state.code.getList()
        maxLength = len(fullList)
        index = fullList.index(instruction)
        startIndex = max(min(index - margin, maxLength - length), 0)
        endIndex = min(startIndex + length, maxLength)
        selectedList = fullList[startIndex:endIndex]
        result = []
        for i in selectedList:
            if i == instruction:
                result.append(indicator+str(i))
            else:
                result.append(space*len(indicator)+str(i))
        return result
