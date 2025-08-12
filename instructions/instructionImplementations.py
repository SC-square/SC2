from instructions.Instruction import Instruction
from evm.State import State
from evm.Variable import Variable
from evm.Type import Type
from instructions.instructionSubClasses import (JumpInstruction,
                                                JumpDestInstruction,
                                                HaltInstruction,
                                                MemoryInstruction,
                                                StackInstruction,
                                                EnvironmentInstruction,
                                                GasInstruction,
                                                CallInstruction,
                                                CopyInstruction)


class STOP(HaltInstruction):
    def _execute(self, state: State):
        return


class ADD(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x + y]


class MUL(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x * y]


class SUB(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x - y]


class DIV(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x / y]


class SDIV(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x.sdiv(y)]


class MOD(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x % y]


class SMOD(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x.smod(y)]


class ADDMOD(Instruction):
    def _execute(self, state: State):
        x, y, n = self._stackInput[0], self._stackInput[1], self._stackInput[2]
        self._stackOutput = [(x + y) % n]


class MULMOD(Instruction):
    def _execute(self, state: State):
        x, y, n = self._stackInput[0], self._stackInput[1], self._stackInput[2]
        self._stackOutput = [(x * y) % n]


class EXP(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x ** y]


class SIGNEXTEND(Instruction):
    def _execute(self, state: State):
        b, x = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x.signextend(b)]


class LT(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x < y]


class GT(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x > y]


class SLT(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x.slt(y)]


class SGT(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x.sgt(y)]


class EQ(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x == y]


class ISZERO(Instruction):
    def _execute(self, state: State):
        x = self._stackInput[0]
        self._stackOutput = [x.isZero()]


class AND(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x & y]


class OR(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x | y]


class XOR(Instruction):
    def _execute(self, state: State):
        x, y = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x ^ y]


class NOT(Instruction):
    def _execute(self, state: State):
        self._stackOutput = [~self._stackInput[0]]


class BYTE(Instruction):
    def _execute(self, state: State):
        i, x = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x.byte(i)]


class SHL(Instruction):
    def _execute(self, state: State):
        # stack top is shift
        s, x = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x << s]


class SHR(Instruction):
    def _execute(self, state: State):
        # stack top is shift
        s, x = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x >> s]


class SAR(Instruction):
    def _execute(self, state: State):
        # stack top is shift
        s, x = self._stackInput[0], self._stackInput[1]
        self._stackOutput = [x.sar(s)]


class SHA3(Instruction):
    def _execute(self, state: State):
        '''
        Stack input:
        - offset: byte offset in the memory.
        - size: byte size to read in the memory.

        Stack output:
        - hash: Keccak-256 hash of the given data in memory.
        '''
        offset = self._stackInput[0].getValue
        size = self._stackInput[1].getValue
        # dummy output, unknown value
        output = Variable()
        if offset is not None and size is not None:
            currOffset = offset
            for _ in range(size//state.memory.WORD_SIZE):
                # load words separately
                variable = state.memory.load(currOffset)
                currOffset += state.memory.WORD_SIZE
                if not variable.isNone:
                    # avoid dummy loaded variable
                    output.addSource(variable)
        self._stackOutput = [output]


class ADDRESS(EnvironmentInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class BALANCE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class ORIGIN(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class CALLER(Instruction):
    def _execute(self, state: State):
        output = Variable(type=Type.MSGSENDER)
        self._stackOutput = [output]


class CALLVALUE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class CALLDATALOAD(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        output = Variable(type=Type.USERINPUT)
        self._stackOutput = [output]


class CALLDATASIZE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class CALLDATACOPY(CopyInstruction):
    def _execute(self, state: State):
        '''
        Stack input:
        - destOffset: byte offset in the memory where the result will be copied.
        - offset: byte offset in the calldata to copy.
        - size: byte size to copy.
        '''
        destOffset = self._stackInput[0]
        offset = self._stackInput[1].getValue
        size = self._stackInput[2].getValue
        # dummy call data
        value = Variable(type=Type.USERINPUT)
        state.memory.store(destOffset, value, size)


class CODESIZE(EnvironmentInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class CODECOPY(CopyInstruction):
    def _execute(self, state: State):
        '''
        Stack input:
        - destOffset: byte offset in the memory where the result will be copied.
        - offset: byte offset in the code to copy.
        - size: byte size to copy.
        '''
        destOffset = self._stackInput[0]
        offset = self._stackInput[1].getValue
        size = self._stackInput[2].getValue
        # dummy code data
        value = Variable(type=Type.CODE)
        state.memory.store(destOffset, value, size)


class GASPRICE(GasInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class EXTCODESIZE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class EXTCODECOPY(CopyInstruction):
    def _execute(self, state: State):
        '''
        Stack input:
        - address: 20-byte address of the contract to query. If address points 
        to an EOF contract, result is as if its code was EF00.
        - destOffset: byte offset in the memory where the result will be copied.
        - offset: byte offset in the code to copy.
        - size: byte size to copy.
        '''
        destOffset = self._stackInput[1]
        offset = self._stackInput[2].getValue
        size = self._stackInput[3].getValue
        # dummy extcode data
        value = Variable(type=Type.EXTCODE)
        state.memory.store(destOffset, value, size)


class RETURNDATASIZE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class RETURNDATACOPY(CopyInstruction):
    def _execute(self, state: State):
        '''
        Stack input:
        - destOffset: byte offset in the memory where the result will be copied.
        - offset: byte offset in the return data from the last executed sub context to copy.
        - size: byte size to copy.
        '''
        destOffset = self._stackInput[0]
        offset = self._stackInput[1].getValue
        size = self._stackInput[2].getValue
        # dummy return data
        value = Variable(type=Type.RETURNDATA)
        state.memory.store(destOffset, value, size)


class EXTCODEHASH(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class BLOCKHASH(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class COINBASE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class TIMESTAMP(EnvironmentInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class NUMBER(EnvironmentInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class DIFFICULTY(EnvironmentInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class GASLIMIT(GasInstruction):
    def _execute(self, state: State):
        self._stackOutput = [Variable(self._GASLIMIT)]


class CHAINID(EnvironmentInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class SELFBALANCE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class BASEFEE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class BLOBHASH(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class BLOBBASEFEE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class POP(Instruction):
    def _execute(self, state: State):
        return  # no action needed


class MLOAD(MemoryInstruction):
    def _execute(self, state: State):
        offset = self._stackInput[0]
        self._stackOutput = [state.memory.load(offset)]


class MSTORE(MemoryInstruction):
    def _execute(self, state: State):
        offset = self._stackInput[0]
        value = self._stackInput[1]
        state.memory.store(offset, value)


class MSTORE8(MemoryInstruction):
    def _execute(self, state: State):
        offset = self._stackInput[0]
        value = self._stackInput[1]
        state.memory.store(offset, value, size=1)


class SLOAD(Instruction):
    def _execute(self, state: State):
        key = self._stackInput[0]
        result = state.storage.load(key)
        self._stackOutput = [result]


class SSTORE(Instruction):
    def _execute(self, state: State):
        key = self._stackInput[0]
        value = self._stackInput[1]
        state.storage.store(key, value)


class JUMP(JumpInstruction):
    def _execute(self, state: State):
        self._setDestination(state)
        if self._destination is not None:
            state.pc = self._destination


class JUMPI(JumpInstruction):
    def _execute(self, state: State):
        self._setDestination(state)
        if self._destination is not None and not self._stackInput[1].equals(Variable(0)):
            state.pc = self._destination


class PC(Instruction):
    def _execute(self, state: State):
        self._stackOutput = [Variable(state.pc)]


class MSIZE(Instruction):
    def _execute(self, state: State):
        self._stackOutput = [Variable(state.memory.getSize)]


class GAS(GasInstruction):
    def _execute(self, state: State):
        remainingGas = self._GASLIMIT - self._INTRINSIC_COST - state.gas - self.getGas
        self._stackOutput = [Variable(remainingGas)]


class JUMPDEST(JumpDestInstruction):
    def _execute(self, state: State):
        return  # no action needed


class TLOAD(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class TSTORE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        return


class MCOPY(CopyInstruction):
    def _execute(self, state: State):
        '''
        Copying takes place as if an intermediate buffer was used, allowing the destination 
        and source to overlap. If size > 0 and (src + size or dst + size) is beyond the 
        current memory size, the memory is extended with respective gas cost applied.

        Stack input:
        - destOffset: byte offset in the memory where the result will be copied.
        - offset: byte offset in the memory from which to copy.
        - size: byte size to copy.
        '''
        destOffset = self._stackInput[0].getValue
        offset = self._stackInput[1].getValue
        size = self._stackInput[2].getValue
        state.memory.copys(destOffset, offset, size)


class PUSH(Instruction):
    def _execute(self, state: State):
        # PUSHx or PUSH0
        self._stackOutput = [Variable(self.getOperand)
                             if self.hasOperand else Variable(0)]


class DUP(StackInstruction):
    def _execute(self, state: State):
        # copy the bottom value of input stack, then put it on top
        self._stackOutput = [self._stackInput[-1]] + self._stackInput
        state.insStack.pushes([self._arguments[-1]] + self._arguments)


class SWAP(StackInstruction):
    def _execute(self, state: State):
        # swap the top and bottom values of input stack
        self._stackOutput = self._stackInput.copy()
        self._stackOutput[0], self._stackOutput[-1] = self._stackOutput[-1], self._stackOutput[0]
        outputInsStack = self._arguments.copy()
        outputInsStack[0], outputInsStack[-1] = outputInsStack[-1], outputInsStack[0]
        state.insStack.pushes(outputInsStack)


class LOG(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        return


class CREATE(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class CALL(CallInstruction):
    '''
    Stack input:
    - gas: amount of gas to send to the sub context to execute. The gas that is not used by the sub context is returned to this one.
    - address: the account which context to execute.
    - value: value in wei to send to the account.
    - argsOffset: byte offset in the memory in bytes, the calldata of the sub context.
    - argsSize: byte size to copy (size of the calldata).
    - retOffset: byte offset in the memory in bytes, where to store the return data of the sub context.
    - retSize: byte size to copy (size of the return data).

    Stack output:
    - success: return 0 if the sub context reverted, 1 otherwise.
    '''

    def _execute(self, state: State):
        inputOffset = self._stackInput[3].getValue
        inputSize = self._stackInput[4].getValue
        outputOffset = self._stackInput[5].getValue
        outputSize = self._stackInput[6].getValue
        self.callFunction(state, inputOffset, inputSize,
                          outputOffset, outputSize)
        # output 1 if successful, else 0
        self._stackOutput = [Variable()]


class CALLCODE(CallInstruction):
    '''
    Stack input:
    - gas: amount of gas to send to the sub context to execute. The gas that is not used by the sub context is returned to this one.
    - address: the account which code to execute.
    - value: value in wei to send to the account.
    - argsOffset: byte offset in the memory in bytes, the calldata of the sub context.
    - argsSize: byte size to copy (size of the calldata).
    - retOffset: byte offset in the memory in bytes, where to store the return data of the sub context.
    - retSize: byte size to copy (size of the return data).

    Stack output:
    - success: return 0 if the sub context reverted, 1 otherwise.
    '''

    def _execute(self, state: State):
        inputOffset = self._stackInput[3].getValue
        inputSize = self._stackInput[4].getValue
        outputOffset = self._stackInput[5].getValue
        outputSize = self._stackInput[6].getValue
        self.callFunction(state, inputOffset, inputSize,
                          outputOffset, outputSize)
        # output 1 if successful, else 0
        self._stackOutput = [Variable()]


class RETURN(HaltInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        return


class DELEGATECALL(CallInstruction):
    '''
    Stack input:
    - gas: amount of gas to send to the sub context to execute. The gas that is not used by the sub context is returned to this one.
    - address: the account which code to execute.
    - argsOffset: byte offset in the memory in bytes, the calldata of the sub context.
    - argsSize: byte size to copy (size of the calldata).
    - retOffset: byte offset in the memory in bytes, where to store the return data of the sub context.
    - retSize: byte size to copy (size of the return data).

    Stack output:
    - success: return 0 if the sub context reverted, 1 otherwise.
    '''

    def _execute(self, state: State):
        inputOffset = self._stackInput[2].getValue
        inputSize = self._stackInput[3].getValue
        outputOffset = self._stackInput[4].getValue
        outputSize = self._stackInput[5].getValue
        self.callFunction(state, inputOffset, inputSize,
                          outputOffset, outputSize)
        # output 1 if successful, else 0
        self._stackOutput = [Variable()]


class CREATE2(Instruction):
    def _execute(self, state: State):
        # TODO: implementation
        self._stackOutput = [Variable()]


class STATICCALL(CallInstruction):
    '''
    Stack input:
    - gas: amount of gas to send to the sub context to execute. The gas that is not used by the sub context is returned to this one.
    - address: the account which context to execute.
    - argsOffset: byte offset in the memory in bytes, the calldata of the sub context.
    - argsSize: byte size to copy (size of the calldata).
    - retOffset: byte offset in the memory in bytes, where to store the return data of the sub context.
    - retSize: byte size to copy (size of the return data).

    Stack output:
    - success: return 0 if the sub context reverted, 1 otherwise.
    '''

    def _execute(self, state: State):
        inputOffset = self._stackInput[2].getValue
        inputSize = self._stackInput[3].getValue
        outputOffset = self._stackInput[4].getValue
        outputSize = self._stackInput[5].getValue
        self.callFunction(state, inputOffset, inputSize,
                          outputOffset, outputSize)
        # output 1 if successful, else 0
        self._stackOutput = [Variable()]


class REVERT(HaltInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        return


class INVALID(HaltInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        return


class SELFDESTRUCT(HaltInstruction):
    def _execute(self, state: State):
        # TODO: implementation
        return


class UNKNOWN(Instruction):
    '''
    instruction with unknown opcode, halt execution in real EVM
    '''

    def _execute(self, state: State):
        return  # ignore, not halting

    def __str__(self) -> str:
        return super().__str__()+':'+hex(self.getOpcode)
