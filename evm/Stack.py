# from evm.Value import Value


class Stack:
    '''
    private class

    `Stack` is a list of Any items
    '''
    LIMIT = 1024  # EVM stack limitation

    def __init__(self, stack: list = None) -> None:
        self._stack = stack if stack is not None else []

    @property
    def getLength(self):
        return len(self._stack)

    def __str__(self) -> str:
        result = self.toStringList()
        return '\n'.join(result)

    def __len__(self) -> int:
        return len(self._stack)

    def __eq__(self, other: object) -> bool:
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            # if type(self._stack[i]) != type(other._stack[i]):
            if not self._stack[i].equals(other._stack[i]):
                return False
        return True

    def __checkUnderflow(self, count: int = 1) -> bool:
        return self.getLength - count < 0

    def __checkOverflow(self, count: int = 1) -> bool:
        return self.getLength + count > Stack.LIMIT

    def pop(self, index: int = -1):
        if self.__checkUnderflow():
            # TODO: Error handler
            print('Error: Stack Underflow Error.')
            return None
        return self._stack.pop(index)

    def push(self, item):
        if self.__checkOverflow():
            # TODO: Error handler
            print('Warning: Stack Overflow Error.')
        self._stack.append(item)

    def pops(self, count: int) -> list:
        '''
        pop multiple items
        '''
        result = []
        if self.__checkUnderflow(count):
            # TODO: Error handler
            print('Error: Stack Underflow Error.')
            return None
        for _ in range(count):
            result.append(self.pop())
        return result

    def pushes(self, items: list):
        '''
        push multiple items in a list
        - parameter: a list of items, 
        the first item is always the top value of stack
        '''
        count = len(items)
        if self.__checkOverflow():
            # TODO: Error handler
            print('Warning: Stack Overflow Error.')
        for _ in range(count):
            self.push(items.pop())

    def __itemToString(self, item) -> str:
        return str(item)

    def toStringList(self) -> list:
        result = []
        for index, item in enumerate(reversed(self._stack)):
            result.append(f"{index + 1}:{self.__itemToString(item)}")
        return result

    def copy(self):
        return Stack(self._stack.copy())
