from signature.Signature import Signature
import json
import os


class SignatureTable(object):
    '''
    A read-only table mapping function selector to signature
    '''
    DEFAULT_FILE = 'signatures.json'

    def __init__(self):
        self.table = {}
        self.__initFromFile()

    def __initFromFile(self):
        currDir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(currDir, SignatureTable.DEFAULT_FILE)
        result = {}
        fp = open(filename)
        data = json.load(fp)
        fp.close()
        for k in data.keys():
            selector = k[2:] if k.startswith('0x') else k
            result[selector.lower()] = Signature(data[k])
        self.table = result

    def __getitem__(self, selector: str):
        '''
        Override `[]` operation
        '''
        return self.table.get(selector, None)
