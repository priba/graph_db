import argparse
import glob
from Element import Element
import shutil
import os

parser = argparse.ArgumentParser(description='Generate a dataset from a given prototype folder.')

# Prototypes
parser.add_argument('--dirPrototypes', help='prototype folder', default=['./prototypes/Letters/', './prototypes/Digits/'])
parser.add_argument('--nodeThreshold', help='prototypes node threshold', default=0.4)

# Dataset
parser.add_argument('--dirDataset', help='dataset folder', default='./dataset/Letters/')
parser.add_argument('--division', help='division (tr, val, te)', default=(5000, 3000, 3000))

args = parser.parse_args()

if __name__ == '__main__':

    # If some dataset is previously created within the same folder, DELETE
    if os.path.isdir(args.dirDataset):
        shutil.rmtree(args.dirDataset)

    # Create folder structure
    os.makedirs(args.dirDataset)
    os.makedirs(args.dirDataset+'train/')
    os.makedirs(args.dirDataset+'validation/')
    os.makedirs(args.dirDataset+'test/')

    # Find prototypes
    proto_files = []
    for i in range(len(args.dirPrototypes)):
        proto_files += glob.glob(args.dirPrototypes[i] + '*.gml')
    num_class = len(proto_files)

    for i in range(num_class):
        el = Element(proto_files[i])

        if args.nodeThreshold is not None:
            el.add_nodes(args.nodeThreshold)

        g = el.distort()