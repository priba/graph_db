from __future__ import division

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
parser.add_argument('--division', help='division (tr, val, te)', default=[300, 300, 300])
parser.add_argument('--unbalanced', action='store_true', default=False, help='Unbalanced database')

# Distortion Node
parser.add_argument('--nodeDisplace', help='node std for distort its position', default=0.1)
parser.add_argument('--nodeAdd', help='node std for adding in a source neighbourhood', default=0.8)

# Distortion Edge
parser.add_argument('--edgeMaximum', help='maximum number of new edges', default=8)
parser.add_argument('--addEdge', help='probability to add new edge', default=0.1)
parser.add_argument('--rmEdge', help='probability to new edge', default=0.1)
parser.add_argument('--edgeConnection', help='new edge connected to existing node', default=0.75)


args = parser.parse_args()


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
        # Random Distribution
        examples_x_class = np.random.random((3, num_class))
        # Normalize, each class sums 1
        examples_x_class = examples_x_class / np.sum(examples_x_class, axis=1)[:, None]
        # Number of examples
        examples_x_class = np.ceil(examples_x_class * np.array(args.division)[:, None])
    else:
        # Balanced distribution of nodes
        examples_x_class = np.tile(np.ceil(np.array(args.division) / num_class)[:,None], (1,num_class))

    # Iterate class prototypes
    for i in range(num_class):
        el = Element(proto_files[i])

        el.set_distortion(args.nodeDisplace, args.nodeAdd, args.edgeMaximum, args.addEdge, args.rmEdge, args.edgeConnection)

        # Add nodes if necessary
        if args.nodeThreshold is not None:
            el.add_nodes(args.nodeThreshold)

        # Create the dataset samples for each set (train, validation, test)
        for s in range(len(f_set)):
            for sample in range(int(examples_x_class[s][i])):
                g = el.distort()
                nx.write_gml(g, args.dirDataset+f_set[s]+str(sample)+'_'+el.get_label()+'.gml')
