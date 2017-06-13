import networkx as nx
from Plotter import plot_graph

import os
import glob

import argparse

parser = argparse.ArgumentParser(description='Process prototype folder.')
parser.add_argument('--dir', help='prototype folder', default='./Letters/')

args = parser.parse_args()

if __name__ == '__main__':
    files = glob.glob(args.dir + '*.gml')
    for f in files:
        g = nx.read_gml(f)
        base = os.path.splitext(f)[0]
        plot_graph(g, save_path=base+'.png')

