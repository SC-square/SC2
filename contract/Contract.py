import re
from contract.Regex import Regex
from contract.VersionChecker import VersionChecker


class Contract:
    def __init__(self, binary: str) -> None:
        self.binary = binary[2:] if binary.startswith('0x') else binary
        self.version = None
        self.strippedBinary = None  # binary without meta
        self.compilationMetadata = None  # meta
        self.constructorRemainingData = None
        self.runtimeBinary = None
        self.constructorBinary = None
        self.childrenContracts = None
        self.metaCount = 0
        self.__parseBinary()

    @property
    def getRuntimeBinary(self) -> str:
        return self.runtimeBinary

    def __splitMeta(self):
        '''
        split the binary using version pattern to get the meta
        binary = strippedBinary + compilationMetadata + constructorRemainingData
        '''
        binary = self.binary
        # initial values
        self.strippedBinary = binary
        self.compilationMetadata = ''
        self.constructorRemainingData = ''
        # if the version is unknown, return
        if not self.version.isKnown:
            return
        self.metaCount = len(re.findall(self.version.getPattern, binary))
        match = re.search(self.version.getPattern, binary)
        if match:
            start, end = match.span()
            self.strippedBinary = binary[:start]
            self.compilationMetadata = binary[start:]
            self.constructorRemainingData = binary[end:]

    def __parseBinary(self):
        '''
        use regex to check the format and version of the contract
        '''
        binary = self.binary
        # whether it is a solidity contract
        solidityCheck = re.search(Regex.SOLIDITY, binary)

        # get version information
        # versionChecker = VersionChecker()
        version = VersionChecker.checkVersions(binary)
        self.version = version

        # split the binary to filter meta data
        self.__splitMeta()

        codeCount = len(re.findall(Regex.RUNTIME, binary))
        if codeCount > self.metaCount:  # constructor existed
            # split constructor and runtime
            # len(splittedStrippedBinary) == 5, if 2 (or more) patterns are found
            # len(splittedStrippedBinary) == 3, if 1 pattern is found
            # len(splittedStrippedBinary) == 1, if 0 pattern is found
            splittedStrippedBinary = re.split(
                Regex.RUNTIME, self.strippedBinary, 2)
            # runtime will be always the last one, no matter the pattern is found or not
            self.runtimeBinary = splittedStrippedBinary[-1]
            self.constructorBinary = splittedStrippedBinary[2] if len(
                splittedStrippedBinary) >= 5 else ''
        else:  # constructor not existed
            self.runtimeBinary = self.strippedBinary
            self.constructorBinary = ''
        # strippedBinary = constructorBinary + runtimeBinary

        splittedRuntimeBinary = re.split(Regex.RUNTIME, self.runtimeBinary, 2)
        if len(splittedRuntimeBinary) == 5:  # if 2 (or more) patterns are found
            # children contracts existed
            self.runtimeBinary = splittedRuntimeBinary[2]
            self.childrenContracts = splittedRuntimeBinary[-1]
        else:
            self.childrenContracts = ''
        # runtimeBinary = runtimeBinary + childrenContracts
        # binary = constructorBinary + runtimeBinary + childrenContracts
        #  + compilationMetadata + constructorRemainingData
