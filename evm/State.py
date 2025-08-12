from evm.Variable import Variable
from evm.Code import Code
from evm.Stack import Stack
from evm.Memory import Memory
from evm.Storage import Storage
from copy import deepcopy


class State:
    '''
    public class
    '''
    NULL = Variable()

    def __init__(self, code: Code, pc: int = 0, stack: Stack = None, insStack: Stack = None, memory: Memory = None, storage: Storage = None, gas: int = 0) -> None:
        self.code = code
        self.pc = pc
        self.stack = stack if stack is not None else Stack()  # Stack of Value
        self.insStack = insStack if insStack is not None else Stack()  # Stack of Instruction
        self.memory = memory if memory is not None else Memory()
        self.storage = storage if storage is not None else Storage()
        self.gas = gas

    def __eq__(self, other: object) -> bool:
        # TODO: memory and storage
        # ignore code and gas
        return self.pc == other.pc and self.stack == other.stack

    def getNext(self):
        return self.code.get(self.pc)

    def copy(self):
        '''
        return a copy State, only Code object is shared
        '''
        return State(self.code, self.pc, deepcopy(self.stack), self.insStack.copy(), deepcopy(self.memory), deepcopy(self.storage), self.gas)
