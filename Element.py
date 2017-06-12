from __future__ import division

import networkx as nx
import numpy as np

from Plotter import plot_graph

class Element:
    def __init__(self, f_name):
        self.el = nx.read_gml(f_name)
        self.label = self.el.graph['class']

    def distort(self):
        return self.el

    def add_nodes(self, d):

        # Create a new graph
        g = nx.Graph()

        # Initialize the nodes given by the prototype
        g.add_nodes_from(self.el.nodes(data=True))

        for s, t, w in self.el.edges_iter(data=True):

            diff_coord = np.array(self.el.node[t]['coord']) - np.array(self.el.node[s]['coord'])

            dist = np.linalg.norm(diff_coord)
            node_to_add = int(dist/d)

            inc = 1/node_to_add

            # Add first node
            g.add_node(len(g.node), {'coord': (inc * diff_coord + self.el.node[s]['coord']).tolist()})
            g.add_edge(s, len(g.node)-1)

            for i in range(2, node_to_add):
                g.add_node(len(g.node), {'coord': (i*inc*diff_coord + self.el.node[s]['coord']).tolist()})
                g.add_edge(len(g.node)-2, len(g.node)-1)

            g.add_edge(len(g.node) - 1, t)
        self.el = g