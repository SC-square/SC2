import re


class Version:
    '''
    private class
    '''

    def __init__(self, name: str, pattern: str) -> None:
        self._name = name
        self._pattern = pattern

    @property
    def getName(self) -> str:
        return self._name

    @property
    def getPattern(self) -> str:
        return self._pattern

    @property
    def isKnown(self) -> bool:
        '''
        retrun Ture if known version
        '''
        return self._pattern != ''

    def checkVersion(self, binary: str) -> bool:
        '''
        check the version using regex
        '''
        return True if re.search(self._pattern, binary) else False
