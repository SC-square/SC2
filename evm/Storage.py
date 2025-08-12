from evm.Variable import Variable


class Storage:
    '''
    Storage model implemented by dict
    '''

    def __init__(self) -> None:
        self._storage = {}

    def load(self, key: Variable) -> Variable:
        if key.hasValue:  # valid value
            return self._storage.get(key.getValue, Variable())
        elif key.hasType:  # type only
            return self._storage.get(key.getType, Variable())
        else:
            return Variable()

    def store(self, key: Variable, value: Variable) -> bool:
        if key.hasValue:  # valid value
            self._storage[key.getValue] = value
            return True
        elif key.hasType:  # type only
            self._storage[key.getType] = value
            return True
        else:
            return False
