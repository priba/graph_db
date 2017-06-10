import networkx as nx
from Plotter import plot_graph

import os
import glob


if __name__ == '__main__':
    files = glob.glob('*.gml')
    for f in files:
        g = nx.read_gml(f)
        base = os.path.splitext(f)[0]
        plot_graph(g, save_path=base+'.png')
