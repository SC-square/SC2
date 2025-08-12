class Signature(object):
    def __init__(self, signature: str):
        '''
        Init the function name and parameters from a signature string,
        suppose the format is: `name(param1,param2,...)`
        '''
        self.raw = signature
        self.name = ''
        self.parameters = []

        words = signature.split('(')
        # the sub-string before '(' is name
        self.name = words[0]
        if len(words) > 1:
            # the sub-string after '(' is parameter string
            parameters = words[1].replace(')', '').strip()
            if len(parameters):
                paramList = parameters.split(',')
                self.parameters = [p.strip() for p in paramList]

    def __str__(self) -> str:
        return self.raw

    @property
    def getName(self) -> str:
        return self.name

    @property
    def getParameters(self) -> list:
        return self.parameters

    @property
    def getParameterNumber(self) -> int:
        return len(self.parameters)
