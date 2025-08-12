from evm.Type import Type


class Variable(object):
    '''
    private class
    '''
    UPPER_BOUND = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    LOWER_BOUND = 0x0
    MOD = UPPER_BOUND+1

    def __init__(self, value: int = None, type: str = None) -> None:
        self._value = value
        self._type = type
        self._source = []

    @property
    def getValue(self) -> int:
        return self._value

    @property
    def getType(self) -> str:
        return self._type

    @property
    def getSource(self) -> list:
        return self._source

    @property
    def hasValue(self):
        return self.getValue is not None

    @property
    def hasType(self):
        return self.getType is not None

    @property
    def isNone(self):
        return not self.hasValue and not self.hasType

    def setType(self, type: str):
        self._type = type

    def addSource(self, source):
        '''
        add variable to the source list, and propagate the type
        '''
        if not any(source is s for s in self._source):
            self._source.append(source)
            self.__propagateType(source)

    def __propagateType(self, other):
        '''
        set the type as the type of other variable if prior
        '''
        newType = Type.getPrior(self.getType, other.getType)
        self.setType(newType)

    def __str__(self) -> str:
        result = hex(self.getValue) if self.hasValue else 'UnknownValue'
        if self.hasType:
            result += f' ({self.getType})'
        return result

    def __signed(self, uint: int) -> int:
        return uint-Variable.MOD if uint > (Variable.UPPER_BOUND >> 4) else uint

    def __bound(self, integer: int) -> int:
        return int(integer) % Variable.MOD

    def __binaryOperation(self, other, operation):
        if self.hasValue and other.hasValue:
            result = Variable(self.__bound(
                operation(self.getValue, other.getValue)))
        else:
            result = Variable()
        result.addSource(self)
        result.addSource(other)
        return result

    def __unaryOperation(self, operation):
        if self.hasValue:
            result = Variable(self.__bound(operation(self.getValue)))
        else:
            result = Variable()
        result.addSource(self)
        return result

    def __signedBinaryOperation(self, other, operation):
        return self.__binaryOperation(other, lambda x, y: operation(self.__signed(x), self.__signed(y)))

    # arithmetic operators
    def __add__(self, other):
        return self.__binaryOperation(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self.__binaryOperation(other, lambda x, y: x - y)

    def __mul__(self, other):
        return self.__binaryOperation(other, lambda x, y: x * y)

    def __truediv__(self, other):
        return self.__binaryOperation(other, lambda x, y: x // y if y != 0 else 0)

    def __mod__(self, other):
        return self.__binaryOperation(other, lambda x, y: x % y)

    def __pow__(self, other):
        if other.hasValue and other.getValue > 255:  # max 2^256-1
            result = Variable()
            result.addSource(self)
            result.addSource(other)
            return result
        return self.__binaryOperation(other, lambda x, y: x ** y)

    # comparison operators
    def __eq__(self, other):
        return self.__binaryOperation(other, lambda x, y: x == y)

    def __lt__(self, other):
        return self.__binaryOperation(other, lambda x, y: x < y)

    def __gt__(self, other):
        return self.__binaryOperation(other, lambda x, y: x > y)

    # bitwise operators
    def __and__(self, other):
        return self.__binaryOperation(other, lambda x, y: x & y)

    def __or__(self, other):
        return self.__binaryOperation(other, lambda x, y: x | y)

    def __xor__(self, other):
        return self.__binaryOperation(other, lambda x, y: x ^ y)

    def __lshift__(self, other):
        return self.__binaryOperation(other, lambda x, y: x << y)

    def __rshift__(self, other):
        return self.__binaryOperation(other, lambda x, y: x >> y)

    # unary operators
    def __invert__(self):
        return self.__unaryOperation(lambda x: (~x) & Variable.UPPER_BOUND)

    def isZero(self):
        return self.__unaryOperation(lambda x: x == 0)

    # signed binary operators
    def sdiv(self, other):
        # int((-1)/2)=0, but (-1)//2=-1
        return self.__signedBinaryOperation(other, lambda x, y: x / y if y != 0 else 0)

    def smod(self, other):
        return self.__signedBinaryOperation(other, lambda x, y: x % y)

    # signed comparison operators
    def slt(self, other):
        return self.__signedBinaryOperation(other, lambda x, y: x < y)

    def sgt(self, other):
        return self.__signedBinaryOperation(other, lambda x, y: x > y)

    # SAR operator
    def sar(self, other):
        # the right operand cannot be negative
        return self.__binaryOperation(other, lambda x, y: self.__signed(x) >> y)

    # SIGNEXTEND
    def __signextend(self, x: int, b: int) -> int:
        signBit = 8 * (b + 1) - 1
        y = x
        if x >> signBit == 1:
            # if sign bit is set, extend the sign
            y = x | ((Variable.UPPER_BOUND << signBit) & Variable.UPPER_BOUND)
        return y

    def signextend(self, b):
        return self.__binaryOperation(b, lambda x, b: self.__signextend(x, b))

    # BYTE
    def __byte(self, x: int, i: int) -> int:
        byteLimit = 32
        if not (0 <= i < byteLimit):
            return 0
        shift = (byteLimit - 1 - i) * 8
        y = (x >> shift) & 0xff
        return y

    def byte(self, i):
        return self.__binaryOperation(i, lambda x, i: self.__byte(x, i))

    # equal Value
    def equals(self, other) -> bool:
        return self.getValue == other.getValue
