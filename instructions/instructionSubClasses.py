from instructions.Opcode import Opcode
from evm.State import State
from evm.Variable import Variable
from instructions.Instruction import Instruction
from signature.SignatureTable import SignatureTable


class HaltInstruction(Instruction):
    '''
    private abstract class

    sub-classes:
    - `STOP`
    - `REVERT`
    - `RETURN`
    - `INVALID`
    - `SELFDESTRUCT`
    '''

    def execute(self, state: State):
        super().execute(state)
        self._setInvalidPC(state)


class JumpDestInstruction(Instruction):
    '''
    private abstract class

    sub-classes:
    - `JUMPDEST`
    '''
    pass


class JumpInstruction(Instruction):
    '''
    private abstract class

    sub-classes:
    - `JUMP`
    - `JUMPI`
    '''

    def __init__(self, offset: int, opcode: Opcode) -> None:
        super().__init__(offset, opcode)
        self._destination = None

    @property
    def getDestination(self) -> int:
        return self._destination

    @property
    def hasSolvedDestination(self) -> int:
        return self._destination is not None

    def setDestination(self, destination: int):
        self._destination = destination

    def _setDestination(self, state: State):
        '''
        set the destination using the stack input Value, 
        must be called in `_execute()`
        '''
        if not len(self._stackInput):
            return
        offset = self._stackInput[0]
        if offset.hasValue:
            pc = offset.getValue
            if isinstance(state.code.get(pc), JumpDestInstruction):
                self.setDestination(pc)

    def toStringWithArgument(self) -> str:
        return super().toStringWithArgument() + ((' ' + hex(self.getDestination)) if self.hasSolvedDestination else ' ?')


class MemoryInstruction(Instruction):
    '''
    private abstract class

    sub-classes:
    - `MLOAD`
    - `MSTORE`
    - `MSTORE8`
    - `CallInstruction`
    '''

    def execute(self, state: State):
        memoryCost = state.memory.getCost()
        super().execute(state)
        self._updateDynamicGas(state, memoryCost)

    def _updateDynamicGas(self, state: State, memoryCost: int):
        dynamicGas = state.memory.getCost() - memoryCost
        state.gas += dynamicGas


class CallInstruction(MemoryInstruction):
    '''
    private abstract class

    sub-classes:
    - `CALL`
    - `CALLCODE`
    - `DELEGATECALL`
    - `STATICCALL`
    '''
    signatureTable = SignatureTable()

    def __init__(self, offset: int, opcode: Opcode) -> None:
        super().__init__(offset, opcode)
        self.selector = None
        self.signature = None

    def execute(self, state):
        # TODO: other operation
        # TODO: calculate the gas
        super().execute(state)

    def __parseSignature(self, callData: str):
        '''
        parse call data to extract function signature, 
        including function name and signature.
        - `callData` (`str`): raw call data loaded from Memory, 
        a bytecode string not starting with '0x'.
        '''
        if len(callData) < 8:
            # no valid function selector
            return
        selector = callData[:8].lower()
        signature = CallInstruction.signatureTable[selector]
        self.selector = selector
        self.signature = signature

    def __typeInference(self, state: State, inputOffset: int, inputSize: int):
        '''
        load parameters from memory, set the types according to signature
        '''
        if inputOffset is None or inputSize is None or self.signature is None:
            return
        offset = inputOffset+8
        parameters = self.signature.getParameters
        for parameterType in parameters:
            if offset+32-inputOffset > inputSize:
                break
            variable = state.memory.load(Variable(offset))
            variable.setType(parameterType)
            offset += 32

    def callFunction(self, state: State, inputOffset: int, inputSize: int, outputOffset: int, outputSize: int):
        '''
        core logic of function call
        '''
        if inputOffset is not None and inputSize is not None:
            callData = state.memory.loadRaw(inputOffset, inputSize)
            self.__parseSignature(callData)
            self.__typeInference(state, inputOffset, inputSize)
        if outputOffset is not None and outputSize is not None:
            # dummy return value
            returnValue = Variable(0)
            state.memory.store(Variable(outputOffset),
                               returnValue, size=outputSize)

    def toStringWithArgument(self) -> str:
        result = super().toStringWithArgument()
        if self.signature:
            result += '\n '+' '*len(result.split()[0])+str(self.signature)
        return result

    def toStringWithSemantic(self):
        '''
        return a string with format "opcode <signature>"

        e.g. "CALL transfer(address,uint256,uint256)"
        '''
        return super().toStringWithSemantic() + (str(self.signature) if self.signature else '')


class CopyInstruction(MemoryInstruction):
    '''
    private abstract class

    sub-classes:
    - `CALLDATACOPY`
    - `CODECOPY`
    - `EXTCODECOPY`
    - `RETURNDATACOPY`
    - `MCOPY`
    '''

    def __init__(self, offset, opcode):
        super().__init__(offset, opcode)


class StackInstruction(Instruction):
    '''
    private abstract class

    sub-classes:
    - `DUP`
    - `SWAP`
    '''

    def toStringWithArgument(self) -> str:
        '''
        Ignore the stack input for `DUP` and `SWAP`.
        '''
        return self.__str__()


class EnvironmentInstruction(Instruction):
    '''
    private abstract class

    sub-classes:
    - `GasInstruction`
    '''
    pass


class GasInstruction(EnvironmentInstruction):
    '''
    private abstract class

    sub-classes:
    - `GASPRICE`
    - `GASLIMIT`
    - `GAS`
    '''

    def __init__(self, offset: int, opcode: Opcode) -> None:
        super().__init__(offset, opcode)
        self._GASLIMIT = 0xffffffffffff
        self._INTRINSIC_COST = 21000
