from cfg.CFG import CFG, BasicBlock, Edge
from evm.Code import Code
from instructions.instructionImplementations import *
from copy import deepcopy


class FSG(CFG):
    APIS = (BLOCKHASH,
            BLOBHASH,
            BASEFEE,
            BLOBBASEFEE,
            CHAINID,
            COINBASE,
            DIFFICULTY,
            GASLIMIT,
            NUMBER,
            TIMESTAMP,
            GAS,
            CALLDATALOAD,
            CALLER,
            CALLVALUE,
            GASPRICE,
            ORIGIN,
            CallInstruction
            )

    def __init__(self, code: Code = None, name: str = 'fsg', cfg: CFG = None) -> None:
        if cfg is None:
            super().__init__(code, name)
        else:
            self._name = cfg._name
            self._filename = cfg._filename
            self._code = cfg._code
            self._nodes = cfg._nodes
            self._edges = cfg._edges
            self._connectedBlocks = cfg._connectedBlocks
            self._showOrphanBlocks = cfg._showOrphanBlocks
        self.APIsubgraph = None
        self.combinedCFG = None

    def getAPIsubgraph(self) -> CFG:
        return self.APIsubgraph

    def getCombinedCFG(self) -> CFG:
        return self.combinedCFG

    def generateAPIsubgraph(self, shiftOffset: bool = True) -> CFG:
        '''
        create an API sub-graph containing only the API instructions
        - `shiftOffset` (`bool`): if `True`, change all offset of blocks
        to offset + code size, to avoid same offset with original graph
        '''
        newCFG = self.copy()
        for block in list(newCFG.getNodes.values()):
            newInstructions = []
            for i in block.getInstructions:
                if isinstance(i, FSG.APIS):
                    newInstructions.append(i)
            block.setInstructions(newInstructions)
            if len(newInstructions) == 0:
                # remove empty block from graph
                newCFG._removeBlock(block)
        if shiftOffset:
            blocks = newCFG.getNodes
            for key in list(blocks.keys()):
                block = blocks.pop(key)
                block.setStartOffset(block.getStartOffset+self.getCode.getSize)
                blocks[block.getStartOffset] = block
        self.APIsubgraph = newCFG
        return newCFG

    def combine(self):
        '''
        combine the original and API graphs
        '''
        APIsubgraph = self.APIsubgraph
        if APIsubgraph is None:
            return
        newCFG = self.copy()
        newCFG.getNodes.update(APIsubgraph.getNodes)
        newCFG.setEdges(newCFG.getEdges + APIsubgraph.getEdges)
        self.combinedCFG = newCFG
        return newCFG
