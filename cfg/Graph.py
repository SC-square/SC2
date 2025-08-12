import abc


class Graph(object):
    '''
    abstract class
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, name: str = 'graph') -> None:
        self._name = name
        self._nodes = None
        self._edges = None

    @property
    def getName(self):
        return self._name

    @property
    def getNodes(self):
        return self._nodes

    @property
    def getEdges(self):
        return self._edges

    def setName(self, name):
        self._nodes = name

    def setNodes(self, nodes):
        self._nodes = nodes

    def setEdges(self, edges):
        self._edges = edges

    @abc.abstractmethod
    def render(self):
        '''
        abstract method
        '''
        raise NotImplementedError("Must be implemented by subclasses")
