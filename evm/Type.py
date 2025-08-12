class Type(object):
    '''
    public static class
    '''
    USERINPUT = 'user input'
    MSGSENDER = 'msg.sender'
    ADDRESS = 'ADDRESS'
    CALLER = 'CALLER'
    CALLDATA = 'CALLDATA'
    CODE = 'CODE'
    EXTCODE = 'EXTCODE'
    RETURNDATA = 'RETURNDATA'

    priority = [USERINPUT, CALLER]

    @staticmethod
    def getPrior(type1: str, type2: str):
        '''
        return type2 if type2 takes priority over type1, else type1
        '''
        if type1 is None or type2 in Type.priority:
            return type2
        else:
            return type1
