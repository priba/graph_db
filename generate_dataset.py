#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    generate_dataset.py
    Generates a dataset providing a set of prototypes. These prototypes are then distorted to generate new elements of the class.
"""

from __future__ import division

import argparse
import glob
import shutil
import os

import networkx as nx
import numpy as np

# Our Modules
from Element import Element

__author__ = "Pau Riba, Anjan Dutta"
__email__ = "priba@cvc.uab.cat, adutta@cvc.uab.cat"

# Argument parser
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
parser.add_argument('--nodeAdd', help='node std for adding a node in a source neighbourhood', default=0.8)

# Distortion Edge
parser.add_argument('--edgeMaximum', help='maximum number of new edges that can be added', default=8)
parser.add_argument('--addEdge', help='probability to add new edge', default=0.1)
<<<<<<< HEAD
parser.add_argument('--rmEdge', help='probability to new edge', default=0.1)
parser.add_argument('--edgeConnection', help='new edge connected to existing node', default=0.75)

=======
parser.add_argument('--rmEdge', help='probability to remove an edge', default=0.1)
parser.add_argument('--edgeConnection', help='probability new edge is connected to an existing node', default=0.75)
>>>>>>> 8e9d650825c2e55037052c0feb1c177246f76217

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

    # Balanced or unbalanced dataset
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

        # Define distortions
        el.set_distortion(args.nodeDisplace, args.nodeAdd, args.edgeMaximum, args.addEdge, args.rmEdge,
                          args.edgeConnection)

        # Add nodes if necessary
        if args.nodeThreshold is not None:
            el.add_nodes(args.nodeThreshold)

        # For each set (train, validation, test)
        for s in range(len(f_set)):
            # Apply random distortion to generate each element
            for sample in range(int(examples_x_class[s][i])):
                g = el.distort()
                nx.write_gml(g, args.dirDataset+f_set[s]+str(sample)+'_'+el.get_label()+'.gml')
