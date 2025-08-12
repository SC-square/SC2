class Node:
    def __init__(self) -> None:
        self._name = None
        self._successors = set()
        self._predecessors = set()

    @property
    def getName(self):
        return self._name

    @property
    def getSuccessors(self) -> set:
        return self._successors

    @property
    def getPredecessors(self) -> set:
        return self._predecessors

    @property
    def hasSuccessors(self) -> bool:
        return bool(len(self._successors))

    @property
    def hasPredecessors(self) -> bool:
        return bool(len(self._predecessors))

    def setName(self, name):
        self._name = name

    def setSuccessors(self, successors: set):
        self._successors = set(successors)

    def setPredecessors(self, predecessors: set):
        self._predecessors = set(predecessors)

    def addSuccessor(self, successor) -> bool:
        if successor not in self._successors:
            self._successors.add(successor)
            return True
        return False

    def addPredecessor(self, predecessor) -> bool:
        if predecessor not in self._predecessors:
            self._predecessors.add(predecessor)
            return True
        return False
