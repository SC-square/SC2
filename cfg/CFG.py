from evm.State import State
from evm.Code import Code
from cfg.Graph import Graph
from cfg.Edge import Edge
from cfg.BasicBlock import BasicBlock
from instructions.instructionImplementations import *
import bisect


class CFG(Graph):
    EDGE_DEFAULT_STYLE = {'fontname': 'Courier', 'fontsize': '30.0'}
    NODE_DEFAULT_STYLE = {'shape': 'box', 'fontname': 'Courier',
                          'fontsize': '30.0', 'rank': 'same'}
    DOT_EXTENSION = '.dot'

    def __init__(self, code: Code = None, name: str = 'cfg', jsonDict: dict = None) -> None:
        super().__init__(name)
        self._filename = name + CFG.DOT_EXTENSION
        self._code = None
        self._nodes = {}
        self._edges = []
        self._connectedBlocks = set()
        # config
        self._showOrphanBlocks = False

        if code is not None:
            self.__initFromCode(code)
        elif jsonDict is not None:
            self.__initFromJson(jsonDict)

    def __initFromCode(self, code: Code):
        self._code = code
        self.__initBasicBlocks()

    def __initFromJson(self, jsonDict: dict):
        # TODO:
        raise NotImplementedError("TBD")
        bytecode = jsonDict["bytecode"]
        nodes = jsonDict["nodes"]
        edges = jsonDict["edges"]

    @property
    def getCode(self) -> Code:
        return self._code

    @property
    def getName(self) -> str:
        return self._name

    def setCode(self, code: Code):
        self._code = code

    def __initBasicBlocks(self):
        result = {}
        curr = BasicBlock()
        for offset, instruction in self._code:
            if isinstance(instruction, JumpDestInstruction) and len(curr):
                result[curr.getName] = curr  # archive block
                curr = BasicBlock()  # new block
            curr.addInstruction(instruction)  # append
            if isinstance(instruction, JumpInstruction) or isinstance(instruction, HaltInstruction):
                result[curr.getName] = curr  # archive block
                curr = BasicBlock()  # new block
        if len(curr):
            result[curr.getName] = curr  # archive block
        self._nodes = result

    def _addEdge(self, from_: BasicBlock, to: BasicBlock, type_, weight: int = 0) -> bool:
        if from_ is None or to is None:
            return False
        edge = Edge(from_, to, type_, weight)
        if edge in self._edges:
            return False
        self._edges.append(edge)
        from_.addSuccessor(to)
        to.addPredecessor(from_)
        self._connectedBlocks.add(from_.getName)
        self._connectedBlocks.add(to.getName)
        return True

    def getBlockByName(self, name: int) -> BasicBlock:
        return self._nodes.get(name, None)

    def buildCFG(self, loopLimit: int = 2, maximized: bool = False):
        '''
        build CFG by BFS
        - `loopLimit` (`int`): the limitation of visit count of each block, to avoid the infinite loop when there are circles in graph
        - `maximized` (`bool`): if `True`, try to traverse the circles at max times until no edge is added after `loopLimit` times
        '''
        stateQueue = [State(self._code)]  # avoid recursion
        blockVisitCnt = {_: 0 for _ in self._nodes.keys()}  # avoid loop
        visitedStates = []  # avoid loop
        while len(stateQueue):
            # the while loop executes instructions in one block
            state = stateQueue.pop(0)
            currOffset = state.pc
            if blockVisitCnt[currOffset] > loopLimit or state in visitedStates:
                continue
            visitedStates.append(state.copy())
            blockVisitCnt[currOffset] += 1
            currBlock = self.getBlockByName(currOffset)
            addedEdge = False
            i = state.getNext()
            while i is not None:
                if isinstance(i, JumpDestInstruction) and i.getOffset != currBlock.getStartOffset:
                    # have normal ins before JUMPDEST
                    stateQueue.append(state.copy())  # push state
                    toBlock = self.getBlockByName(i.getOffset)
                    addedEdge = self._addEdge(currBlock, toBlock,
                                              Edge.NORMAL, state.stack.getLength)  # add edge
                    break  # break before execution
                i.execute(state)  # execute instruction to solve jump target
                if isinstance(i, HaltInstruction) or isinstance(i, JumpInstruction):  # halt
                    if isinstance(i, JumpInstruction):
                        # false branch
                        if isinstance(i, JUMPI):
                            falseBranchOffset = i.getNextOffset()
                            toFalseBlock = self.getBlockByName(
                                falseBranchOffset)
                            addedEdge = self._addEdge(currBlock, toFalseBlock,
                                                      Edge.FALSE, state.stack.getLength)  # add edge
                            state.pc = falseBranchOffset
                            stateQueue.append(state.copy())  # False branch
                        # true branch or jump destination
                        jumpTargetOffset = i.getDestination
                        if jumpTargetOffset is None:
                            # unsolved jump destination
                            break
                        edgeType = Edge.TRUE if isinstance(
                            i, JUMPI) else Edge.JUMP
                        toTrueBlock = self.getBlockByName(jumpTargetOffset)
                        addedEdge = self._addEdge(currBlock, toTrueBlock,
                                                  edgeType, state.stack.getLength)  # add edge
                        state.pc = jumpTargetOffset
                        stateQueue.append(state.copy())
                    break  # break after execution
                i = state.getNext()
            if maximized and addedEdge:
                # in maximized mode, clear count if new edges are added
                blockVisitCnt = {
                    _: 0 for _ in self._nodes.keys()}

    def getOrphanBlocks(self) -> list:
        result = []
        for block in self._nodes.values():
            if block.isOrphan:
                result.append(block)
        return result

    def getUnsolvedJump(self) -> list:
        result = []
        for block in self._nodes.values():
            for i in block.getInstructions:
                if isinstance(i, JumpInstruction) and not i.hasSolvedDestination:
                    result.append(i)
        return result

    def getAdjacencyMatrix(self):
        import numpy as np
        nodeToIndex = {n[1]: i for i, n in enumerate(
            sorted(self._nodes.items()))}
        matrix = np.eye(len(self._nodes))
        for edge in self._edges:
            matrix[nodeToIndex[edge.getFrom],
                   nodeToIndex[edge.getTo]] = edge.getWeight
        return matrix

    def findInstrcutionPositionByOffset(self, offset: int) -> tuple:
        if offset < 0:
            return None
        nodeNames = list(self._nodes.keys())
        nodeNameindex = bisect.bisect_right(nodeNames, offset) - 1
        nodeName = nodeNames[nodeNameindex]
        node = self.getBlockByName(nodeName)
        offsets = [i.getOffset for i in node.getInstructions]
        index = bisect.bisect_left(offsets, offset)
        if index == len(offsets) or offsets[index] != offset:
            return None
        return (nodeName, index)

    def render(self, showOrphanBlocks: bool = False):
        from graphviz import Digraph
        g = Digraph(name=self._name, filename=self._filename)
        g.node_attr = CFG.NODE_DEFAULT_STYLE
        g.edge_attr = CFG.EDGE_DEFAULT_STYLE
        g.attr(rankdir='TB')
        with g.subgraph(name='CFG') as c:
            for node in self._nodes.values():
                if not node.isOrphan:
                    self._renderNode(c, node)
            for edge in self._edges:
                self._renderEdge(c, edge)
        if showOrphanBlocks:
            with g.subgraph(name='OrphanBlocks') as o:
                for node in self._nodes.values():
                    if node.isOrphan:
                        self._renderNode(o, node)
        g.render()

    def _renderNode(self, graph, node: BasicBlock):
        label = node.instructionsToString().replace('\n', '\l')+'\l'
        graph.node(name=hex(node.getName), label=label)

    def _renderEdge(self, graph, edge: Edge):
        color = 'black'  # default
        if edge.getType == Edge.TRUE:
            color = 'green'
        elif edge.getType == Edge.FALSE:
            color = 'red'
        elif edge.getType == Edge.JUMP:
            color = 'blue'
        graph.edge(str(edge.getFrom), str(
            edge.getTo), label=str(edge.getWeight), color=color)

    def printNodes(self):
        for k, v in self._nodes.items():
            print(f"{v}: \n{v.instructionsToString()}")

    def printEdges(self):
        for edge in self._edges:
            print(edge)

    def toBinaryString(self) -> str:
        return self._code.toBinaryString()

    def getOpcodeSequence(self, includeOperand: bool = False) -> list:
        return self._code.getOpcodeSequence(includeOperand)

    def toJson(self, showOrphanBlocks: bool = False, simplified: bool = False, semantic: bool = False) -> dict:
        '''
        convert cfg to json according to EtherSolve format
        - `showOrphanBlocks` (`bool`): include the orphan nodes if `True`
        - `simplified` (`bool`): exclude the raw bytecode attributes if `True`
        - `semantic` (`bool`): use semantic annotation for instructions if `True`
        '''
        result = {}
        if not simplified:
            # add bytecode if not simplified
            result["bytecode"] = self.toBinaryString()
        # add nodes
        nodes = []
        for k, v in sorted(self._nodes.items()):
            if not v.isOrphan or showOrphanBlocks:
                nodes.append(v.toJson(simplified, semantic))
        result["nodes"] = nodes
        # add edges
        edges = []
        for edge in self._edges:
            edges.append(edge.toJson())
        result["edges"] = edges

        return result

    def copy(self):
        # init new CFG, create new blocks
        newCFG = CFG(code=self.getCode, name=self.getName)
        newCFG._showOrphanBlocks = self._showOrphanBlocks
        # reconnect new blocks via existing edges
        for edge in self.getEdges:
            fromName = edge.getFrom.getName
            toName = edge.getTo.getName
            from_ = newCFG.getBlockByName(fromName)
            to = newCFG.getBlockByName(toName)
            newCFG._addEdge(from_, to, type_=edge.getType,
                            weight=edge.getWeight)
        return newCFG

    def _removeBlock(self, block: BasicBlock):
        # classify edges
        inEdges = {}
        outEdges = {}
        removeEdges = []
        for edge in self.getEdges:
            if edge.getFrom is block or edge.getTo is block:
                removeEdges.append(edge)
            if edge.getFrom is block and edge.getTo is block:  # self-loop edge
                continue
            elif edge.getFrom is block:  # out edge
                outEdges[edge.getTo] = edge
            elif edge.getTo is block:  # in edge
                inEdges[edge.getFrom] = edge
        # reconnect predecessors and successors
        # fully connect edges
        for p in block.getPredecessors:
            if p is block:
                continue
            inEdge = inEdges.get(p, None)
            inWeight = inEdge.getWeight if inEdge else 0
            for s in block.getSuccessors:
                if s is block:
                    continue
                outEdge = outEdges.get(s, None)
                outWeight = outEdge.getWeight if outEdge else 0
                self._addEdge(from_=p, to=s, type_=Edge.COMBINE,
                              weight=inWeight+outWeight)
        # remove edges
        for e in removeEdges:
            self._removeEdge(e)
        # remove block
        self.getNodes.pop(block.getName, None)

    def _removeEdge(self, edge: Edge):
        try:
            self.getEdges.remove(edge)
        except:
            pass
        from_ = edge.getFrom
        to = edge.getTo
        fromSuccessors = from_.getSuccessors
        toPredecessors = to.getPredecessors
        if to in fromSuccessors:
            fromSuccessors.remove(to)
        if from_ in toPredecessors:
            toPredecessors.remove(from_)
