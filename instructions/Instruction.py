import abc  # is
from instructions.Opcode import Opcode  # has
from evm.State import State  # use


class Instruction(object):
    '''
    private abstract class
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, offset: int, opcode: Opcode) -> None:
        self._offset = offset
        self._opcode = opcode
        self._operand = None
        self._stackInput = []
        self._stackOutput = []
        self._arguments = []

    @property
    def getOffset(self) -> int:
        '''
        return offset
        '''
        return self._offset

    @property
    def getOpcode(self) -> int:
        '''
        return opcode ID
        '''
        return self._opcode.opcode

    @property
    def getName(self) -> str:
        '''
        return opcode name
        '''
        return self._opcode.name

    @property
    def getOperandSize(self) -> int:
        '''
        return operand size in bytes
        '''
        return self._opcode.operandSize

    @property
    def getStackPopSize(self) -> int:
        '''
        return stack pop size
        '''
        return self._opcode.stackPopSize

    @property
    def getStackPushSize(self) -> int:
        '''
        return stack push size
        '''
        return self._opcode.stackPushSize

    @property
    def getGas(self) -> int:
        '''
        return gas cost
        '''
        return self._opcode.gas

    @property
    def getOperand(self) -> int:
        '''
        return operand
        '''
        return self._operand

    @property
    def getArguments(self) -> list:
        '''
        return the arguments, a list of `Instruction`
        '''
        return self._arguments

    @property
    def getSize(self) -> int:
        '''
        return instruction size in bytes
        '''
        return Opcode.SIZE + self.getOperandSize

    @property
    def getStackBalance(self) -> int:
        '''
        return stack balance, i.e. number of generated variables in stack
        '''
        return self.getStackPushSize - self.getStackPopSize

    @property
    def hasOperand(self) -> bool:
        return bool(self.getOperandSize)

    def setOffset(self, offset: int):
        self._offset = offset

    def setOperand(self, operand: int):
        self._operand = operand

    def getNextOffset(self):
        return self._offset + self.getSize

    def __str__(self) -> str:
        '''
        defualt string format

        return a string with format: "offset: opcode <operand>"

        e.g. "0x1: PUSH1 0x0"
        '''
        return f"{hex(self._offset)}: {self.getName}" + (f" {hex(self._operand)}" if self.hasOperand else '')

    def toBinaryString(self) -> str:
        '''
        for opcode sequence generation

        return a binary opcode string

        e.g. "PUSH1 0x0" -> "6000"
        '''
        return f"{self.getOpcode:02x}" + (f"{self._operand:0{self.getOperandSize*2}x}" if self.hasOperand else '')

    def toStringWithArgument(self) -> str:
        '''
        for PDF generation

        return a string appending the stack input if not None

        the arguments are presented by the offsets of input instructions

        e.g. 
        0x1: PUSH0
        0x2: PUSH0
        0x3: MSTORE(0x2,0x1)
        '''
        result = self.__str__()
        if self.getStackPopSize:
            arguments = []
            for argument in self.getArguments:
                arguments.append(hex(argument.getOffset))
            result += f"({','.join(arguments)})"
        return result

    def toStringWithSemantic(self) -> str:
        '''
        return string with semantic annotation, vary with sub-classes

        default: "opcode <operand>"
        '''
        result = ''
        if self.getStackPushSize == 1 and len(self._stackOutput):
            variable = self._stackOutput[0]
            if variable.getType:
                result += variable.getType + ' = '
        result += f"{self.getName}" + \
            (f" {hex(self._operand)}" if self.hasOperand else '')
        return result

    def _setInvalidPC(self, state: State):
        state.pc = -2

    def execute(self, state: State):
        # pop from stack
        stackInput = state.stack.pops(self.getStackPopSize)
        arguments = state.insStack.pops(self.getStackPopSize)
        if stackInput is None or arguments is None:
            # if stack underflow, then halt
            self._setInvalidPC(state)  # halt
            return

        self._stackInput = stackInput
        self._arguments = arguments
        try:
            self._execute(state)
        except Exception as e:
            # TODO: Error handler
            # print(f'Error: {e}')
            pass
        if len(self._stackOutput) != self.getStackPushSize:
            # TODO: Error handler
            # print('Error: Instruction Execution Error.')
            self._stackOutput = [State.NULL]*self.getStackPushSize
        state.stack.pushes(self._stackOutput.copy())  # shallow copy
        if self.getStackPushSize == 1:
            state.insStack.push(self)
        state.pc += self.getSize
        state.gas += self.getGas

    @abc.abstractmethod
    def _execute(self, state: State):
        '''
        abstract method for arithmetic instruction execution
        - parameter: the VM state
        '''
        raise NotImplementedError("Must be implemented by subclasses")
