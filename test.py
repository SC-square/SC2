from stellargraph.mapper import PaddedGraphGenerator
from stellargraph import StellarDiGraph
from Dataset import Dataset
import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
import gc
import os

VULS = ['shadowing-state', 'suicidal', 'uninitialized-state', 'arbitrary-send',
        'controlled-array-length', 'controlled-delegatecall', 'reentrancy-eth',
        'unchecked-transfer', 'erc20-interface', 'incorrect-equality',
        'locked-ether', 'mapping-deletion', 'shadowing-abstract', 'tautology',
        'write-after-write', 'constant-function-asm', 'constant-function-state',
        'divide-before-multiply', 'reentrancy-no-eth', 'tx-origin',
        'unchecked-lowlevel', 'unchecked-send', 'uninitialized-local',
        'unused-return', 'incorrect-modifier', 'shadowing-builtin',
        'shadowing-local', 'variable-scope', 'void-cst']


MODELBASE = 'models/'
MODEL = 'SC2'
MODELPATH = f'{MODELBASE}{MODEL}/'
DATASET = f'/path/to/dataset'
DATATYPE = ['pla', 'obf'][0]
LOGPATH = f'logs/{MODEL}/'
WEIGHTED = True
SYMMETRIC = False


def getUSEmodel(path):
    x = tf.keras.layers.Input(shape=[], dtype=tf.string)
    embedded_sequences = hub.KerasLayer(path, trainable=True)(x)
    model = tf.keras.models.Model(
        inputs=x,
        outputs=embedded_sequences
    )
    print(embedded_sequences)
    return model


def getGraphs(dataset: Dataset, USEmodel):
    graphs = []
    for gnx, nodeindices, features in dataset.graphs:
        tf.random.set_seed(seed=0)
        nodefeatures = USEmodel(tf.convert_to_tensor(features))
        nodefeatures = (np.array(nodefeatures)).T
        d = {}
        for i, nodefeature in enumerate(nodefeatures):
            d["f{0}".format(i)] = nodefeature
        node_features = pd.DataFrame(d, index=nodeindices)
        graph = StellarDiGraph.from_networkx(gnx,
                                             node_features=node_features,
                                             node_type_default="basic block",
                                             edge_type_default="--"
                                             )
        graphs.append(graph)
    return graphs


def predict(vul, dataset):
    gcnPath = MODELPATH+vul+'/GCN/'
    usePath = MODELPATH+vul+'/USE/'

    USEmodel = getUSEmodel(usePath)
    GCNmodel = tf.keras.models.load_model(gcnPath)

    graphs = getGraphs(dataset, USEmodel)
    gen = PaddedGraphGenerator(graphs=graphs)
    test_gen = gen.flow(graphs,
                        batch_size=1,
                        symmetric_normalization=SYMMETRIC,
                        weighted=WEIGHTED
                        )
    print('graphs inited, starting test...')
    y_hat = GCNmodel.predict(test_gen, verbose=0).ravel()

    # free up memory
    del GCNmodel
    del USEmodel
    del graphs
    tf.keras.backend.clear_session()
    gc.collect()
    return y_hat


def dumpResult(vul, result):
    import os
    path = LOGPATH
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f'{path}{DATATYPE}.{vul}.log', 'w') as lg:
        for y in result:
            lg.write(str(y)+'\n')


def testAll():
    dataset = Dataset(DATASET, WEIGHTED)
    print('dataset inited')
    for vul in VULS:
        if not os.path.isdir(MODELPATH+vul):
            print(f'Warning: path not found: {MODELPATH+vul}')
            print('skipping...')
            continue
        y_hat = predict(vul, dataset)
        # print(y_hat.T)
        dumpResult(vul, y_hat)
        print('finished: ', vul)
    print('done')


def testOne(index: int):
    vul = VULS[index]
    if not os.path.isdir(MODELPATH+vul):
        print(f'Warning: path not found: {MODELPATH+vul}')
        print('skipping...')
        return
    dataset = Dataset(DATASET, WEIGHTED)
    print('dataset inited:', len(dataset.graphs))
    y_hat = predict(vul, dataset)
    # print(y_hat.T)
    dumpResult(vul, y_hat)
    print('finished: ', vul)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        index = sys.argv[1]
        index = int(index)
        testOne(index)
    else:
        testAll()
