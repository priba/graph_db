import argparse
import glob
import networkx as nx
from Element import Element
import shutil
import os
import numpy as np

parser = argparse.ArgumentParser(description='Generate a dataset from a given prototype folder.')

# Prototypes
parser.add_argument('--dirPrototypes', help='prototype folder', default=['./prototypes/Letters/'])
parser.add_argument('--nodeThreshold', help='prototypes node threshold', default=None)

# Dataset
parser.add_argument('--dirDataset', help='dataset folder', default='./dataset/Letters/')
parser.add_argument('--division', help='division (tr, val, te)', default=(5000, 3000, 3000))
parser.add_argument('--unbalanced', action='store_true', default=False, help='Unalanced dataset')

# Distortion
# TODO

args = parser.parse_args()


def normalize(g):
    coord = [v['coord'] for k, v in g.nodes(data=True)]
    coord = np.array(coord)
    g.graph['mean'] = np.mean(coord, axis=0)
    g.graph['std'] = np.std(coord, axis=0)

    return g

if __name__ == '__main__':

    # If some dataset is previously created within the same folder, DELETE
    if os.path.isdir(args.dirDataset):
        shutil.rmtree(args.dirDataset)

    # Create folder structure
    os.makedirs(args.dirDataset)
    f_set = ['train/', 'validation/', 'test/']
    os.makedirs(args.dirDataset+f_set[0])
    os.makedirs(args.dirDataset+f_set[1])
    os.makedirs(args.dirDataset+f_set[2])

    # Find prototypes
    proto_files = []
    for i in range(len(args.dirPrototypes)):
        proto_files += glob.glob(args.dirPrototypes[i] + '*.gml')
    num_class = len(proto_files)

    if args.unbalanced:
        pass
    else:
        pass

    for i in range(num_class):
        el = Element(proto_files[i])

        if args.nodeThreshold is not None:
            el.add_nodes(args.nodeThreshold)

        for s in range(len(f_set)):
            for sample in range():
                g = el.distort()
                g = normalize(g)
                nx.write_gml(g, args.dirDataset+f_set[s])