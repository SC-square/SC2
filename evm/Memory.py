from evm.Variable import Variable


class Memory:
    '''
    Memory model implemented by str
    '''
    WORD_SIZE = 32

    def __init__(self) -> None:
        self._memory = ''
        self._size = 0  # memory size in bytes, multiple of word size
        self._variables = {}  # store variable objects using offset as keys

    def __str__(self) -> str:
        return self._memory

    @property
    def getSize(self) -> int:
        return self._size

    def __expansion(self, words: int = 1):
        self._size += Memory.WORD_SIZE * words
        self._memory += '0' * (Memory.WORD_SIZE * 2 * words)

    def __checkExpansion(self, offset: int, size: int = WORD_SIZE) -> bool:
        if offset + size > self._size:
            # ceildiv
            words = (offset + size - self._size +
                     Memory.WORD_SIZE - 1) // Memory.WORD_SIZE
            self.__expansion(words)
            return True
        return False

    def __intToStr(self, value: int, size: int = WORD_SIZE) -> str:
        return f"{value:0{size*2}x}"[:size*2]

    def loadRaw(self, offset: int, size: int = WORD_SIZE) -> str:
        '''
        Load raw data from memory with specific offset and size, return string
        '''
        self.__checkExpansion(offset, size)
        data = self._memory[offset*2:(offset+size)*2]
        return data

    def loads(self, offset: int) -> int:
        self.__checkExpansion(offset)
        data = self._memory[offset*2:(offset+Memory.WORD_SIZE)*2]
        return int(data, 16)

    def stores(self, offset: int, value: int, size: int = WORD_SIZE) -> bool:
        self.__checkExpansion(offset, size)
        self._memory = self._memory[:offset*2] + \
            self.__intToStr(value, size) + \
            self._memory[(offset+size)*2:]
        return True

    def copys(self, dest: int, offset: int, size: int) -> bool:
        self.__checkExpansion(offset, size)
        self.__checkExpansion(dest, size)
        self._memory = self._memory[:dest*2] + \
            self._memory[offset*2:(offset+size)*2] + \
            self._memory[(dest+size)*2:]
        return True

    def load(self, offset: Variable) -> Variable:
        if offset.hasValue:  # valid offset
            value = self.loads(offset.getValue)
            variable = self._variables.get(offset.getValue, Variable())
            if variable.hasValue and variable.getValue == value:
                # if variable == value loaded in memory
                return variable
            else:
                # create a new variable
                result = Variable(value)
                if variable.hasType:
                    result.setType(variable.getType)
                return result
        elif offset.hasType:  # valid offset type
            return self._variables.get(offset.getType, Variable())
        else:
            return Variable()

    def store(self, offset: Variable, value: Variable, size: int = WORD_SIZE) -> bool:
        if offset.hasValue:  # valid offset
            if value.hasValue:  # valid offset and value
                self.stores(offset.getValue, value.getValue, size)
            self._variables[offset.getValue] = value
            return True
        elif offset.hasType:  # valid offset type
            self._variables[offset.getType] = value
            return True
        else:
            return False

    def getCost(self) -> int:
        # ceildiv
        sizeWord = (self._size + Memory.WORD_SIZE - 1) // Memory.WORD_SIZE
        cost = (sizeWord ** 2) // 512 + (3 * sizeWord)
        return cost

    def toStringList(self) -> list:
        memoryString = str(self)
        wordLength = Memory.WORD_SIZE * 2
        return [memoryString[i:i + wordLength] for i in range(0, len(memoryString), wordLength)]
