import json
import re
import pandas as pd
import networkx as nx

DATAPATH = '/path/to/dataset'


class Dataset:
    def __init__(self, csvFile=DATAPATH, weighted: bool = True) -> None:
        self.file = csvFile
        self.graphs = []
        self.labels = {}
        self.mulHotLabels = None
        self.init(weighted)

    def init(self, weighted: bool = True):
        df = pd.read_csv(self.file)
        print('file loaded.')
        self.mulHotLabels = df.iloc[:, 2:].values
        for vul in df.columns[2:]:
            labels = df[vul]
            self.labels[vul] = labels
        for _, row in df.iterrows():
            graph = self.jsonToNx(row['cfg'], weighted)
            self.graphs.append(graph)
        print('init finished.')

    def jsonToNx(self, jsonStr: str, weighted: bool = True):
        patterns = [r'(0x)*[0-9]*: ', r':*0x[0-9|a-f]*']
        gnx = nx.DiGraph()
        data = json.loads(jsonStr)
        nodeindices = []
        features = []
        for edge in data['edges']:
            if weighted:
                gnx.add_edge(edge['from'], edge['to'], weight=edge['weight'])
            else:
                gnx.add_edge(edge['from'], edge['to'])
        for node in data['nodes']:
            if weighted:
                gnx.add_edge(node['offset'], node['offset'],
                             weight=1)  # self loop
            else:
                gnx.add_edge(node['offset'], node['offset'])  # self loop
            nodeindices.append(node['offset'])
            ops = node['parsedOpcodes']
            # remove offset and operand (or unknown opcode)
            ops = ops.replace('\n', ' ')
            for p in patterns:
                ops = re.sub(p, '', ops)
            ops = ' '.join(ops.split())
            features.append(ops)
        return gnx, nodeindices, features
