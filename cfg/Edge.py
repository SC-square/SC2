class Edge:
    NORMAL = 'NORMAL'
    JUMP = 'JUMP'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    COMBINE = 'COMBINE'

    def __init__(self, from_, to, type_: str, weight: int = 0) -> None:
        self._from = from_
        self._to = to
        self._type = type_
        self._weight = weight

    @property
    def getFrom(self):
        return self._from

    @property
    def getTo(self):
        return self._to

    @property
    def getType(self) -> str:
        return self._type

    @property
    def getWeight(self) -> int:
        return self._weight

    def __str__(self) -> str:
        return f"[{self._from}] -{self._weight}-> [{self._to}] ({self._type})"

    def __eq__(self, other: object) -> bool:
        return str(self._from) == str(other._from) and str(self._to) == str(other._to)

    def toJson(self) -> dict:
        '''
        convert edge to json according to EtherSolve format
        '''
        result = {}
        result["from"] = self._from.getStartOffset
        result["to"] = self._to.getStartOffset
        result["weight"] = self._weight
        return result
